from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re

title = sys.argv[1]
api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
username = api.call('user')['login']
issue = api.call('create_issue', owner='bodyshopbidsdotcom', repo='snapsheet', data={
  'title': title,
  'assignee': username
})

branch_name = str(issue['number']) + '-' + re.sub('[\s+\:]+', '-', issue['title'].strip().lower())

git = Repo(os.getcwd()).git
git.checkout('HEAD', b=branch_name)
