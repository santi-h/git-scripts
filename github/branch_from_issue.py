from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re
import Helper

api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
issue = None
owner, repo = Helper.owner_and_repo()
if len(sys.argv) <= 1:
  issue = api.call('list_issues', org=owner)[0][0]
else:
  issue = api.call('list_issue', owner=owner, repo=repo, number=sys.argv[1])[0]

branch_name = Helper.branch_name(issue)
Helper.create_branch(branch_name)
