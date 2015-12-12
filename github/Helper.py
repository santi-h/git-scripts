import git
import re
import os

def branch_name(issue):
  return str(issue['number']) + '-' + re.sub('[^\w\d]+', '-', issue['title'].strip().lower())[0:30].strip('-')

def create_branch(branch_name):
  g = git.Repo(os.getcwd()).git
  g.checkout('HEAD', b=branch_name)

def issue_number_from_branch():
  ret = None
  branch = current_branch()
  match = re.search('^(\d+)\-', branch)
  if match is not None:
    ret = int(match.group(1))
  return ret

def owner_and_repo():
  g = git.cmd.Git(os.getcwd())
  remotes = g.execute(['git','remote','-v'])
  match = re.search('github\.com:([\w\-]+)\/([\w\-]+)\.git \(fetch\)', remotes)
  owner = None
  repo = None
  if match is not None:
    owner = match.group(1).encode('ascii')
    repo = match.group(2).encode('ascii')

  return owner, repo

def current_branch():
  return str(git.Repo(os.getcwd()).active_branch)

def push_private():
  repo = git.Repo(os.getcwd())
  remote = repo.remotes['origin']
  remote.push([repo.active_branch, '-f'])
  return repo.active_branch

def local_sha(branch=current_branch()):
  g = git.Repo(os.getcwd()).git
  return g.rev_parse(branch)

def has_conflicts():
  g = git.Repo(os.getcwd()).git
  exception_raised = False
  res = None
  try:
    res = g.merge('master', no_commit=True, no_ff=True)
  except git.exc.GitCommandError:
    exception_raised = True

  if res != 'Already up-to-date.':
    g.merge(abort=True)

  return exception_raised

def origin_sha(branch=current_branch()):
  g = git.Repo(os.getcwd()).git
  return re.search(r'^([^\s]+)\s', g.ls_remote(['origin', branch])).group(1)

def branch_contains(branch='master'):
  g = git.Repo(os.getcwd()).git
  return current_branch() in g.branch(contains='master').split()

