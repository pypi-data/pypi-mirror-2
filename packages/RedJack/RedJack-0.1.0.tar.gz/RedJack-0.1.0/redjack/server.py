#!/usr/bin/python
from __future__ import print_function, division
from future_builtins import *
import sys
import os
import re
import subprocess
import datetime
import time
import yaml
import json
import httplib
import sqlite3
import pprint
import codecs
import logging
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mako.template import Template

from triggers import trigger_classes

default_fmt = "%(asctime)s  %(name)-12s %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=default_fmt,
                    stream=sys.stdout)

log = logging.getLogger("rj.server")

def initiate_triggers(cfg):
    for pn, proj in cfg.get_projects():
        triggers = []
        for idx, trigger in enumerate(proj.pcfg['monitor']['triggers']):
            trigger_type = proj.get_val(trigger, 'type')
            if not trigger_type in trigger_classes:
                raise Exception("trigger %s is not supported" % trigger['type'])
            trigger = cfg.replace_variables_recur(proj.pcfg, trigger)
            t = trigger_classes[trigger_type](proj, trigger_type, trigger, idx)
            t.prepare()
            triggers.append(t)
        proj.pcfg['monitor']['triggers'] = triggers

class Job(object):
    STATE_INIT = "init"
    STATE_EXECUTING = "executing"
    STATE_COMPLETED = "completed"

    def __init__(self, proj, root, job_info, idx):
        self.proj = proj
        self.root = root
        self.job_info = job_info
        self.idx = idx
        self.state = Job.STATE_INIT

        self._save_state()

    def _save_state(self):
        if self.state != Job.STATE_COMPLETED:
            self.proj.crsr.execute("INSERT OR REPLACE INTO jobs (build, idx, command, state) VALUES (?,?,?,?)", 
                                   (self.proj.label, self.idx, "cmd...", self.state))
        else:
            self.proj.crsr.execute("INSERT OR REPLACE INTO jobs (build, idx, command, state, completion_status, exitcode, logfile) VALUES (?,?,?,?,?,?,?)", 
                                   (self.proj.label, self.idx, "cmd...", self.state, self.completion_status, self.exitcode, "logfilepath..."))
        self.proj.conn.commit()
        
    def _pick_machine(self):
        if not 'machine' in self.job_info:
            self.machine = self.root['machines']['any']['localhost']
        else:
            machine = None
            for group, machines in self.root['machines']:
                if self.job_info['machine'] in machines:
                    machine = machines[self.job_info['machine']]
                    break
            if machine == None:
                machine = self.root['machines']['any']['localhost']
            self.machine = machine

    def _agent_send(self, uri, data):
        conn = httplib.HTTPConnection(self.machine['ip-address'], self.machine['port'])
        conn.request("PUT", uri, data)
        try:
            resp = conn.getresponse()
        except Exception, e:
            log.exception(e)
        body = resp.read()
        conn.close()
        #log.info(body)
        #log.info(resp.status)
        # TODO: check status

    def _agent_recv(self, uri):
        conn = httplib.HTTPConnection(self.machine['ip-address'], self.machine['port'])
        conn.request("GET", "/status")
        try:
            resp = conn.getresponse()
        except Exception, e:
            log.exception(e)
        body = resp.read()
        conn.close()
        #log.info(">>>%s<<<" % body)
        #log.info(resp.status)
        # TODO: check status
        return body

    def start(self):
        self._pick_machine()
        log.info("%s: starting job '%s' on machine %s" % (self.proj.name, str(self.job_info), self.machine['ip-address']))
        self._agent_send("/job", json.dumps(dict(self.job_info)))
        self.state = Job.STATE_EXECUTING
        self._save_state()

    def update_state(self):
        body = self._agent_recv("/status")
        self.status = json.loads(body)
        if self.status['state'] == 'completed':
            log.info("%s: job '%s' is completed" % (self.proj.name, str(self.job_info)))
            self.state = Job.STATE_COMPLETED
            self.exitcode = self.status['exitcode']
            self.completion_status = self.status['completion_status']
            self._save_state()

            self.execlog = self._agent_recv("/job-log")
            f = codecs.open(os.path.join(self.proj.bdir, "job-%d.txt" % self.idx), "wt", "utf-8")
            f.write(self.execlog)
            f.close()
            log.debug("%s\n%s\n%s" % ("v"*50, self.execlog, "^"*50))
        self._save_state()


class Project(object):
    def __init__(self, name, cfg, pcfg):
        self.cfg = cfg
        self.name = name
        self.pcfg = pcfg

        # setup database
        if not os.path.isdir(name):
            os.makedirs(name)
        self.conn = sqlite3.connect('%s/%s.db' % (name, name))
        self.crsr = self.conn.cursor()
        self.crsr.execute("CREATE TABLE IF NOT EXISTS project (field TEXT UNIQUE, value TEXT)") # stored fields: version
        self.crsr.execute("""CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY,
                                                              build TEXT NOT NULL,
                                                              idx INTEGER NOT NULL,
                                                              command TEXT NOT NULL,
                                                              state TEXT NOT NULL,
                                                              completion_status TEXT,
                                                              exitcode INTEGER,
                                                              logfile TEXT,
                                                              CONSTRAINT u UNIQUE (build, idx))""")
        self.crsr.execute("""CREATE TABLE IF NOT EXISTS triggers (id INTEGER PRIMARY KEY,
                                                                  type TEXT NOT NULL,
                                                                  idx INTEGER NOT NULL,
                                                                  state BLOB,
                                                                  CONSTRAINT u UNIQUE (type, idx))""")
        self.conn.commit()

        # set initial project params from config
        self.version = 0
        init_label = self.get_val(self.pcfg, 'initial-label')
        init_num = init_label.split("_")[-1].split("-")[-1].split(".")[-1]
        self.label_prefix = init_label[:-len(init_num)]
        self._set_version(int(init_num))

        # initiate runtime state
        self.last_build = None
        self._build_steps = []

        # synchronize state with database
        self._load_state()
        self._save_state()

    def _save_state(self):
        self.crsr.execute("INSERT OR REPLACE INTO project (field, value) VALUES ('version',?)", (str(self.version),))
        self.conn.commit()
    
    def _load_state(self):
        self.crsr.execute("SELECT value FROM project WHERE field='version'")
        ver = self.crsr.fetchone()
        if ver != None:
            self._set_version(int(ver[0]))

    def get_val(self, branch, variable, default=None):
        log.debug(">>>> get_val br:  %s" % str(branch))
        log.debug(">>>> get_val var:  %s" % str(variable))
        if variable in branch:
            val = branch[variable]
        else:
            return default
        if isinstance(val, basestring):
            vals = [val]
        elif isinstance(val, list):
            vals = val
        elif isinstance(val, bool):
            return val
        else:
            raise Exception("unsupported value type %s" % str(type(val)))

        new_vals = []
        for val in vals:
            if re.search("\${%s}" % variable, val) != None:
                raise Exception("recursive variable substitution")
            extra_vars = dict(version=self.version)
            val = self.cfg.replace_variables(extra_vars, val)
            val = self.cfg.replace_variables(self.pcfg, val)
            val = self.cfg.replace_variables(self.cfg.root, val)
            log.debug(">>>> get_val val:  %s" % str(val))
            new_vals.append(val)

        if isinstance(val, basestring):
            val = new_vals[0]
        elif isinstance(val, list):
            val = new_vals

        if variable in ['interval', 'quiet-period']:
            if val.endswith("s"):
                val = int(val[:-1])
            elif val.endswith("m"):
                val = int(val[:-1]) * 60
            elif val.endswith("h"):
                val = int(val[:-1]) * 60 * 60
            else:
                raise Exception('unsupported time unit in value %s of %s' % (val, variable))

        return val

    def _set_version(self, version):
        self.version = version
        self.label = "%s%s" % (self.label_prefix, self.version)

    def _do_build(self, root):
        log.info("%s: do build" % self.name)
        self.last_build = datetime.datetime.now()
        self._set_version(self.version + 1)
        self._save_state()
        self.bdir = os.path.join(self.name, self.label)
        if not os.path.exists(self.bdir):
            os.makedirs(self.bdir)
        for idx, job in enumerate(self.pcfg['build']['jobs']):
            job2 = {}
            for k in job.iterkeys():
                v = self.get_val(job, k)
                #log.info("job: %s === %s" % (v, v2))
                job2[k] = v

            if not "directory" in job2:
                directory = self.get_val(self.pcfg['build'], 'directory')
                if directory != None:
                    job2["directory"] = directory

            self._build_steps.append(Job(self, root, job2, idx))

        self._build_steps[0].start()

    def _check_build(self):
        log.info("%s: check status of build execution" % self.name)
        all_completed = True
        self.successful = True
        for i, job in enumerate(self._build_steps):
            if job.state == Job.STATE_EXECUTING:
                job.update_state()
            if job.state == Job.STATE_COMPLETED:
                if job.completion_status != "ok":
                    log.info("%s: build failed" % self.name)
                    all_completed = True
                    self.successful = False
                    break
                if i + 2 > len(self._build_steps):
                    break
                next_job = self._build_steps[i+1]
                if next_job.state == Job.STATE_INIT:
                    next_job.start()
            else:
                all_completed = False
        
        if all_completed:
            self._do_report()
            self._old_build_steps = self._build_steps
            self._build_steps = []
    
    def _render_report(self):
        header_tpl = """
        <html><head>
        <style type="text/css">
          * {
          font: normal 13px Verdana, Arial, sans-serif;
          }
          h2 {
          font-weight: bold;
          font-size: 18px;
          }
          h3 {
          font-weight: bold;
          font-size: 14px;
          //background: #0f0;
          padding: 3px 0;
          margin: 0px;
          width: 960px;
          text-indent: 5px;
          background: #ccf;
          border-top: 0px;
          border-left: 0px;
          border-right: 0px;
          border-bottom: 1px solid #22f;
          }
          .section {
          width: 960px;
          margin: 15px 0 0 0;
          border: 1px solid #22f;
          }
          table {
          border: 0px;
          width: 960px;
          border-collapse: collapse;
          border-spacing: 0px 0px;
          }
          th {
          font-style: italic;
          font-size: 14px;
          text-align: left;
          padding: 2px 2px 2px 3px;
          border: 2px solid white;
          background: #ff6;
          }
          td {
          padding: 0 0 0 3px;
          border: 2px solid white;
          vertical-align: top;
          }
          tr:nth-child(even) {
          background: #ffc;
          }
          tr:nth-child(odd) {
          background: #ffa;
          }
        </style>
        </head>
        <body>
        <h2>${subject}</h2>
        <div class='section'><h3>Build info</h3>
          <table>
            <tr><td>Date of build: </td><td>${date}</td></tr>
            <!--<tr><td>Build time: </td><td>???</td></tr>-->
            <tr><td>Label: </td><td>${label}</td></tr>
          </table>
        </div>
        """
        html = ""
        # prepare header info
        header_tpl = Template(header_tpl)
        if self.successful:
            subject = "%s Build Successful: %s" % (self.name.capitalize(), self.label)
        else:
            subject = "%s Build Failed: %s" % (self.name.capitalize(), self.label)
        context = {"project": self.name.capitalize(), "successful": self.successful, "date": datetime.datetime.now().strftime("%Y.%m.%d %H:%M"),
                   "label": self.label, "subject": subject}
        header = header_tpl.render(**context)
        html += header

        # get triggers info
        for trigger, changes, report in self.changes:
            html += report

        # get jobs info

        html += "</body></html>"

        log.debug(html)
        f = open(os.path.join(self.bdir, "report.html"), "w")
        f.write(html)
        f.close()

        return subject, "", html

    def _build_email(self, subject, text, html, from_addr, to_addrs):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ", ".join(to_addrs)

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        return msg.as_string()

    def _send_report(self, subject, text, html):
        report_cfg = self.pcfg['report']
        if not 'email' in report_cfg:
            return
        email_cfg = report_cfg['email']

        # get dest email addresses        
        if 'to' in email_cfg:
            to_addrs = self.get_val(email_cfg, 'to')
        if isinstance(to_addrs, basestring):
            to_addrs = [to_addrs]
        # TODO: include-authors

        if 'from' in email_cfg:
            from_addr = self.get_val(email_cfg, 'from')
        else:
            from_addr = 'missing@example.com'

        subject_prefix = self.get_val(email_cfg, 'subject-prefix', "")
        if subject_prefix:
            subject = "%s %s" % (subject_prefix, subject)
        mail = self._build_email(subject, text, html, from_addr, to_addrs)

        # get credentials
        username = None
        password = None
        if 'credentials' in email_cfg:
            credentials = self.get_val(email_cfg, 'credentials')
            f = open(credentials)
            for line in f.readlines():
                field, val = line.split("=")
                field = field.strip()
                val = val.strip()
                if field == "username":
                    username = val
                if field == "password":
                    password = val

        # The actual mail send  
        smtpaddr = self.get_val(email_cfg, 'smtp')
        server = smtplib.SMTP(smtpaddr)
        tls = self.get_val(email_cfg, 'tls')
        if tls:
            server.starttls()  
        if username != None and password != None:
            server.login(username, password)  
        
        server.sendmail(from_addr, to_addrs, mail)  
        server.quit()  

    def _do_report(self):
        subject, text, html = self._render_report()
        self._send_report(subject, text, html)

    def _check_triggers(self):
        self.changes = []
        fire = False
        for trigger in self.pcfg['monitor']['triggers']:
            changes, report = trigger.get_changes()
            if changes != None:
                fire = True
            self.changes.append((trigger, changes, report))
        return fire

    def check_build(self, root):
        # if build is being executed
        if len(self._build_steps) > 0:
            self._check_build()
            return
        
        # otherwise start build if needed
        if self.last_build:
            now = datetime.datetime.now()
            dt = now - self.last_build
            if dt > datetime.timedelta(seconds=self.get_val(self.pcfg['monitor'], 'interval')):
                if self._check_triggers():
                    self._do_build(root)
            else:
                log.info("%s: check build: nothing" % self.name)
        else:
            self._check_triggers()
            self._do_build(root)

class Config(object):
    def _replace_variables2(self, root, branch):
        if isinstance(branch, basestring):
            for var in re.findall("\${(.*?)}", branch):
                if var in root:
                    val = root[var]
                    branch = branch.replace("${%s}" % var, val)
                else:
                    raise Exception("cannot find value for variable %s" % var)
        elif isinstance(branch, dict):
            for k, v in branch.iteritems():
                branch[k] = self._replace_variables(root, v)
        elif isinstance(branch, list):
            branch = [ self._replace_variables(root, v) for v in branch ]
        return branch

    def replace_variables_recur(self, pcfg, branch):
        if isinstance(branch, basestring):
            val = branch
            val = self.replace_variables(pcfg, val)
            val = self.replace_variables(self.root, val)
            return val
        elif isinstance(branch, dict):
            for k, v in branch.iteritems():
                branch[k] = self.replace_variables_recur(pcfg, v)
        elif isinstance(branch, list):
            branch = [ self.replace_variables_recur(pcfg, v) for v in branch ]
        else:
            raise Exception("unrecognized node type %s" % str(type(branch)))
        return branch

    def replace_variables(self, branch, value):
        if not isinstance(value, basestring):
            return value
        #log.info("replace_variables", branch, value, type(value))
        for var_name in re.findall("\${(.*?)}", value):
            if not var_name in branch:
                continue
            val = branch[var_name]
            val = self.replace_variables(branch, val)
            if branch != self.root:
                val = self.replace_variables(self.root, val)
            val = self.replace_variables(branch, val)
            value = value.replace("${%s}" % var_name, str(val))
        return value

        
    def _load_project(self, name, fname):
        pcfg1 = yaml.load(open(fname))
        exts = pcfg1.get('extends', [])
        pcfg = {}
        for ext in exts:
            log.info(ext)
            e = yaml.load(open(ext))
            pcfg.update(e)
        pcfg.update(pcfg1)

        #pcfg = self._replace_variables(pcfg, pcfg)

        p = Project(name, self, pcfg)
        return p

    def load_config(self):
        cfg = yaml.load(open("config.rj"))
        #cfg2 = yaml.load(open(cfg['extends']))
        #cfg2.update(cfg)

        # process machines
        for name, machine in cfg['machines'].iteritems():
            # do ping 
            pass
        cfg['machines']['any'] = {'localhost': {'ip-address': '127.0.0.1', 'port': 8081}}

        self.root = cfg

        # process projects
        projs = {}
        for pn, proj in cfg['projects'].iteritems():
            projs[pn] = self._load_project(pn, proj)
        cfg['projects-states'] = projs

    def get_projects(self):
        return self.root['projects-states'].iteritems()

class Scheduler(object):
    def __init__(self, cfg):
        self.cfg = cfg

        for pn, proj in cfg.get_projects():
            interval = proj.get_val(proj.pcfg['monitor'], 'interval')

    def run(self):
        while True:
            for pn, proj in self.cfg.get_projects():
                proj.check_build(self.cfg.root)

            time.sleep(5)

def main():
    cfg = Config()
    cfg.load_config()

    initiate_triggers(cfg)

    localhost = cfg.root['machines']['any']['localhost']
    #cmd = "python rjagent.py %s %d" % (localhost['ip-address'], localhost['port'])
    #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    s = Scheduler(cfg)
    s.run()



if __name__ == "__main__":
    main()
