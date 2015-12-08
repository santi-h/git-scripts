from GithubAPIGateway import GithubAPIGateway
import Helper
import os
import sys
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--title")
parser.add_argument("-b", "--body")
parser.add_argument("-o", "--open", action="store_true")
args = parser.parse_args()

title = None
if args.title is not None:
  if len(args.title) < 5:
    print "The title should be 5 characters or longer"
    parser.print_usage()
    sys.exit(2)
  else:
    title = args.title

body = None
issue_number = Helper.issue_number_from_branch()
if args.body is not None:
  body = args.body
else:
  body = 'closes #{0}'.format(issue_number)

branch = Helper.push_private()
api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
owner, repo = Helper.owner_and_repo()
if title is None:
  issue = api.call('list_issue', owner=owner, repo=repo, number=issue_number)[0]
  title = '{0} {1}'.format(issue_number, issue['title'])
pr, status = api.call('create_pr', owner=owner, repo=repo, data={
  'title': title,
  'head': str(branch),
  'base': 'master',
  'body': 'closes #{0}'.format(issue_number)
})

print pr['html_url']
if args.open:
  webbrowser.open(pr['html_url'])
