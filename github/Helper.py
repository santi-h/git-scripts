import git
import re
import os

def branch_name(issue):
  return str(issue['number']) + '-' + re.sub('[^\w\d]+', '-', issue['title'].strip().lower())[0:30].strip('-')

def create_branch(branch_name):
  g = git.Repo(os.getcwd()).git
  g.checkout('HEAD', b=branch_name)

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
