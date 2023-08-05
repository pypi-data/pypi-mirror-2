import os
import pickle
import logging
import re
import time
from mako.template import Template

try:
    import mercurial 
    from mercurial import node, commands, hg, ui
except ImportError:
    mercurial = None

try:
    import git
except ImportError:
    git = None
    

log = logging.getLogger("rj.triggers")


class Trigger(object):
    def __init__(self, project, trigger_type, trigger, idx):
        self.project = project
        self.trigger_type = trigger_type
        self.idx = idx
        self._load_state()

    def prepare(self, project):
        pass

    def get_changes(self):
        raise Exception("not implemented")

    def _load_state(self):
        self.project.crsr.execute("SELECT state FROM triggers WHERE type=? and idx=?", (self.trigger_type, self.idx))
        state = self.project.crsr.fetchone()
        if state:
            #log.info("load state", state[0])
            self.state = pickle.loads(str(state[0]))
        else:
            self.state = {}

    def _save_state(self):
        state = pickle.dumps(self.state)
        #log.info("save state", state)
        self.project.crsr.execute("INSERT OR REPLACE INTO triggers (type, idx, state) VALUES (?,?,?)", (self.trigger_type, self.idx, state))
        self.project.conn.commit()

class GitRepo(Trigger):
    def __init__(self, project, trigger_type, repo_info, idx):
        Trigger.__init__(self, project, trigger_type, repo_info, idx)

        if git == None:
            raise Exception("missing git")

        self.url = repo_info['url']
        self.directory = repo_info['directory']

#        return dumper.represent_mapping(cls.yaml_tag, dict(url=repo.url, directory=repo.directory))

    def prepare(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        elif not os.path.isdir(self.directory):
            raise Exception("%s should be a directory" % self.directory)

        if os.path.exists(os.path.join(self.directory, ".git")):
            log.info("git repo already exists in %s" % self.directory)
            return

        g = git.cmd.Git(self.directory)
        g.clone(self.url, self.directory)

        # TODO: set state
        self._save_state()

    def get_changes(self):
        pass

class MercurialRepo(Trigger):
    def __init__(self, project, trigger_type, repo_info, idx):
        Trigger.__init__(self, project, trigger_type, repo_info, idx)

        if mercurial == None:
            raise Exception("missing mercurial")

        self.url = repo_info['url']
        self.directory = repo_info['directory']

#        return dumper.represent_mapping(cls.yaml_tag, dict(url=repo.url, directory=repo.directory))

    def prepare(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        elif not os.path.isdir(self.directory):
            raise Exception("%s should be a directory" % self.directory)

        self.ui = ui.ui()

        if not os.path.exists(os.path.join(self.directory, ".hg")):
            commands.clone(self.ui, self.url, self.directory)
        
        self.repo = hg.repository(self.ui, self.directory)
        self._update_state()

    def _update_state(self):
        tip = self.repo.changelog.tip()
        tip_info = self.repo.changelog.read(tip)
        tip_rev = node.hex(tip)
        self.state["tip"] = tip_rev
        self._save_state()

    def _prepare_report(self, changes):
        tpl = """
        <div class='section'><h3>Changes from Mercurial repositry ${url}</h3>
        <table>
          <tr><th>Author</th><th>Date</th><th>Comment</th><th>Modified files</th></tr>
          % for cs in changesets:
            <tr><td>
            % if cs['email'] != "":
             <a href='mailto:${cs["email"]}'>${cs['author']}</a>
            % else:
             ${cs['author']}
            % endif
            </td><td>${cs['date']}</td><td>${cs['comment']}</td><td>
            % for f in cs['files']:
              ${f}<br/>
            % endfor
            </td></tr>
          % endfor
        </table>
        </div>
        """
        changesets = []
        for rev, change in changes:
            # parse author and his email
            m = re.search("(.*?)<(.*@.*)>", change[1])
            if m != None:
                author = m.group(1).strip()
                email = m.group(2).strip()
            elif "@" in change[1]:
                author = change[1]
                email = change[1]
            else:
                author = change[1]
                email = ""
            # parse date
            t = change[2][0]
            date = time.strftime("%Y.%m.%d<br/>%H:%M", time.localtime(t))

            c = {"revision": rev, "author": author, "email": email, "date": date, "comment": change[4], "branch": change[5],
                 "files": change[3]}
            changesets.append(c)
            #repo.manifest.read(change[0])
        tpl = Template(tpl)
        context = {"url": self.url, "changesets": changesets}
        html = tpl.render(**context)
        return html

    def _get_changes(self):
        remote = hg.repository(self.ui, self.url)
        self.repo.pull(remote)
        commands.update(self.ui, self.repo)
        tip = node.bin(self.state["tip"])
        log.debug("old tip: %s,  new tip %s" % (self.state["tip"], node.hex(self.repo.changelog.tip())))
        changes = []
        for r in reversed(self.repo.changelog.nodesbetween()[0]):
            if r == tip:
                break
            c = self.repo.changelog.read(r)
            #log.debug("%s, %s" % str(node.hex(c[0])), str(c))
            changes.append((r, c))
        log.info("%s: changes %d" % (self.project.name, len(changes)))
        
        if len(changes) > 0:
            self._update_state()
            return changes, self._prepare_report(changes)
        
        return None, self._prepare_report(changes)

    def get_changes(self):
        try:
            return self._get_changes()
        except Exception, e:
            log.exception(e)
        return None, ""

trigger_classes = {"git": GitRepo,
                   "mercurial": MercurialRepo}
