from git import Repo
import re
import os

def branch_name(issue):
  return str(issue['number']) + '-' + re.sub('[^\w\d]+', '-', issue['title'].strip().lower())[0:30].strip('-')

def create_branch(branch_name):
  git = Repo(os.getcwd()).git
  git.checkout('HEAD', b=branch_name)
