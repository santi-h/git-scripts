from GithubAPIGateway import GithubAPIGateway
import Helper
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--description")
parser.add_argument("title")
args = parser.parse_args()
if len(args.title) < 5:
  print "The title should be 5 characters or longer"
  parser.print_usage()
  sys.exit(2)

api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
username = api.call('user')[0]['login']

data = {
  'title': args.title,
  'assignee': username
}

if args.description is not None:
  data.update(body=args.description)

owner, repo = Helper.owner_and_repo()
issue = api.call('create_issue', owner=owner, repo=repo, data=data)[0]

branch_name = Helper.branch_name(issue)
Helper.create_branch(branch_name)
print issue['html_url']
