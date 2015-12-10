from WrikeAPIGateway import WrikeAPIGateway
from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import re
import Helper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nobranch", action="store_true")
parser.add_argument("taskid")
args = parser.parse_args()

def create_issue(task):
  api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
  username = api.call('user')[0]['login']
  body = '### {0}\n___\n\n{1}'.format(task['permalink'].encode('utf-8'), task['description'].encode('utf-8'))
  owner, repo = Helper.owner_and_repo()
  issue = api.call('create_issue', owner=owner, repo=repo, data={
    'title': task['title'],
    'assignee': username,
    'body': body
  })[0]
  return issue

def create_branch(issue):
  branch_name = str(issue['number']) + '-' + re.sub('[^\w\d]+', '-', issue['title'].strip().lower())[0:30].strip('-')
  git = Repo(os.getcwd()).git
  git.checkout('HEAD', b=branch_name)
  return branch_name

api = WrikeAPIGateway()
task = api.call('get_task', id=args.taskid)[0]['data'][0]
issue = create_issue(task)
if args.nobranch == False:
  create_branch(issue)
print issue['html_url']
api.redirect(issue['html_url'])
