from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re

api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
issue = None
if len(sys.argv) <= 1:
  issue = api.call('list_issues', org='bodyshopbidsdotcom')[0]
else:
  issue = api.call('list_issue', owner='bodyshopbidsdotcom', repo='snapsheet', number=sys.argv[1])

branch_name = str(issue['number']) + '-' + re.sub('[\s+\:]+', '-', issue['title'].strip().lower())

git = Repo(os.getcwd()).git
git.checkout('HEAD', b=branch_name)