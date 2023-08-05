#!/usr/bin/python
#
# Copyright 2007 Michal Nowikowski
#
import socket
import os
import os.path
import threading
import random
import time
import Queue
import imp
import inspect
import zipimport
import sys
#import sha
import platform
import subprocess
import logging
import signal
import traceback
import select
import json
import BaseHTTPServer

#from rj.common import client, XMLRPCServer

default_fmt = "%(asctime)s  %(name)-12s %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=default_fmt,
                    stream=sys.stdout)

log = logging.getLogger("rj.agent")


class RjHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            status = self.server.agent.get_job_status()
            status["jobLogUri"] = "/job-log"
            status["newJobUri"] = "/job"
            body = json.dumps(status)
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.send_header("Content-length", str(len(body)))
        elif self.path == '/job-log':
            body = self.server.agent.get_job_log()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(body)))
        else: 
            self.send_error(404)
            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)
            return

        self.end_headers()
        self.wfile.write(body)

        # shut down the connection
        self.wfile.flush()
        self.connection.shutdown(1)


    def do_PUT(self):
        if self.path != "/job":
            log.info("wrong path")
            self.send_error(400)
            return
        size = int(self.headers['Content-Length'])
        body = self.rfile.read(size)
        log.debug("do put %s" % body)

        try:
            data = json.loads(body)
            self.server.agent.start_job(data)
            log.debug("do put completed")
        except:
            self.send_error(400)
            return            

        self.send_response(200)
        #self.send_header("Content-type", "text/xml")
        #self.send_header("Content-length", str(len(response)))
        #self.end_headers()
            
        # shut down the connection
        self.wfile.flush()
        self.connection.shutdown(1)


log = logging.getLogger("agent")

import gc
#gc.set_debug(gc.DEBUG_LEAK)

#from guppy import hpy
#h=hpy()
#import guppy.heapy.RM

    
class Capabilities:
    def __init__(self):
        self.caps = {}
        caps = self.caps
        caps['arch'] = platform.architecture()[0]
        caps['system'] = platform.system()
        caps['libc'] = "-".join(platform.libc_ver())
        caps['machine'] = platform.machine()
        caps['node'] = platform.node()
        caps['platform'] = platform.platform()
        caps['processor'] = platform.processor()
        #caps['python_build'] = platform.python_build()
        #caps['python_compiler'] = platform.python_compiler()
        caps['system_release'] = platform.release()
        caps['system_version'] = platform.version()

        if caps['system'] == "Linux":
            caps['linux_dist'] = "-".join(platform.dist())
            for key in ["USER", "GROUP", "HOME", "PATH", "LANG", "OSTYPE", "PYTHONPATH", "HOST", "MACHTYPE"]:
                if os.environ.has_key(key):
                    caps[key] = os.environ[key]
        elif caps['system'] == "Windows":
            caps['win32_ver'] = "-".join(platform.win32_ver())
            for key in ["USERNAME", "USERDOMAIN", "HOMEPATH", "PATH", "COMPUTERNAME", "OS"]:
                caps[key] = os.environ[key]
        elif caps['system'] == "Mac":
            caps['mac_ver'] = platform.mac_ver()

        self._check_prog("python", "python -V", lambda t: t.split()[1])
        self._check_prog("java", "java -version", lambda t: t.split()[2].strip("\""))
        self._check_prog("perl", "perl -v", lambda t: t.split()[3][1:])
        self._check_prog("gcc", "gcc -dumpversion", lambda t: t)
        
        log.info("Agent capabilities:")
        for key, val in caps.iteritems():
            log.info("\t%s: %s" % (key, str(val)))

    def _popen(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        err = p.wait()
        txt = ""
        if err == 0:
            txt = p.stdout.read().strip()
        return err, txt

    def _check_prog(self, prog, cmd, func):
        err, txt = self._popen(cmd)
        if err == 0:
            self.caps[prog] = func(txt)

    def get(self):
        return self.caps

class Agent(object):
    def __init__(self, ip_address, port):
        log.info("starting agent")
        self.ip_address = ip_address
        self.port = port

        self.rp = None
        self.finish = False

        try:
            signal.signal(signal.SIGINT, self.__keyboard_interrupt_handler)
        except:
            pass

        #self.caps = Capabilities()
        self._setup_http_server()
        
        self._restart()
        self.restart = False

    def run(self):
        log.info("agent started serving")
        # Run the server's main loop
        while not self.finish:
            try:
                iwtd, owtd, ewtd = select.select([self.server.socket], [], [], 5)
            except select.error, e:
                if e[0] == 4: # Interrupted system call, in bg Ctrl-C handler is called and finish flags is set
                    continue
            except:
                log.exception("Exception in select")
                continue
            if iwtd:
                self.server.handle_request()
            if self.restart:
                self.restart = False
                self._restart()

    def _setup_http_server(self):
        # Create server
        BaseHTTPServer.HTTPServer.allow_reuse_address = True
        self.server = BaseHTTPServer.HTTPServer((self.ip_address, self.port), RjHTTPRequestHandler)
        #self.server.socket.settimeout(5) # non-blocking does not work in Windows - requires more work
        self.server.agent = self

    def _restart(self):
        self.queue = Queue.Queue()
        self.rp = RequestProcessor(self.queue, self)

    def __keyboard_interrupt_handler(self, signum, frame):
        #log.info('Signal handler called with signal', signum)
        log.info("manual stop")
        self._quit()

    def _validate_job(self, job):
        commands = ["exec"]
        found = False
        for cmd in commands:
            if cmd in job:
                found = True
                break
        if not found:
            status = "unsupported command"
            log.info("job validating: %s" % status)
            return status
        else:
            log.debug("job validating: ok")
            return None

    def start_job(self, job):
        log.info("start job %s" % str(job))
        status = self._validate_job(job)
        if status:
            return status
        self.queue.put(job)
        return None

    def get_job_status(self):
        log.info("get job status")
        return self.rp.read_status()

    def get_job_log(self):
        log.info("get job log")
        return self.rp.read_log()

    def _quit(self):
        log.info("finish in 5 secs")
        self.server.server_close()
        if self.rp:
            self.rp.finish = True
        self.finish = True

#     def sepuku(self):
#         log.info("sepuku")
#         while not self.queue.empty():
#             time.sleep(5)
#         self._quit()
#         return True


class RequestProcessor(threading.Thread):
    def __init__(self, queue, agent):
        threading.Thread.__init__(self)
        self.finish = False
        self.queue = queue
        self.agent = agent
        self.start()
        self.status = ("waiting", 0, "")

    def run(self):
        while not self.finish:
            try:
                job = self.queue.get(True, 5)
            except Queue.Empty:
                continue
            try:
                self._handle_job(job)
            except Exception, e:
                log.exception(e)
                log.error("connection to server broken - try to reconnect")
                self.agent.restart = True
                break
            except:
                log.exception("unexpected exception occured")
                self.agent._quit()
                break

    def _handle_job(self, job):
        log.info("doing the job")
        self.status = ("starting", 0, "", "")
        if "exec" in job:
            if "directory" in job:
                directory = job["directory"]
            else:
                directory = os.getcwd()
            try:
                p = subprocess.Popen(job["exec"], shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except Exception, e:
                self.status = ("completed", 0, "exception", str(e))
                return
            self.status = ("started", 0, "", "")
            exitcode = p.wait()
            execlog = p.stdout.read()
            if exitcode == 0:
                completion_status = "ok"
            else:
                completion_status = "failed"
            self.status = ("completed", exitcode, completion_status, execlog)

    def read_status(self):
        status = dict(state=self.status[0],
                      exitcode=self.status[1],
                      completion_status=self.status[2])
        return status

    def read_log(self):
        return self.status[-1]

def main():
    a = Agent(sys.argv[1], int(sys.argv[2])) 
    a.run()


if __name__ == '__main__':
    main()
