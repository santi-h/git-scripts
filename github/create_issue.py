from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re

title = sys.argv[1]
api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
username = api.call('user')[0]['login']
issue = api.call('create_issue', owner='bodyshopbidsdotcom', repo='snapsheet', data={
  'title': title,
  'assignee': username
})[0]

branch_name = str(issue['number']) + '-' + re.sub('[\s+\:\.\,\;]+', '-', issue['title'].strip().lower())[0:30].strip('-')

git = Repo(os.getcwd()).git
git.checkout('HEAD', b=branch_name)
print issue['html_url']
