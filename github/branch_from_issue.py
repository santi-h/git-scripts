from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re

api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
issue_number = sys.argv[1]
issue_title = api.call('list_issue', owner='bodyshopbidsdotcom', repo='snapsheet', number=issue_number)['title']

branch_name = issue_number + '-' + re.sub('\s+', '-', issue_title.strip())

git = Repo(os.getcwd()).git
git.checkout('HEAD', b=branch_name)
