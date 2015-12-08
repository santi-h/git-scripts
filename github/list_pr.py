from GithubAPIGateway import GithubAPIGateway
import Helper
import os
import sys
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--open", action="store_true")
args = parser.parse_args()

api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
owner, repo = Helper.owner_and_repo()
branch = str(Helper.current_branch())
prs = api.call('list_pr', owner=owner, repo=repo, data={
  'head': branch
})[0]
url = None
for pr in prs:
  if pr['head']['ref'] == branch:
    url = pr['html_url']
    break

if url is not None:
  print url
  if args.open:
    webbrowser.open(url)
else:
  print "No PRs on this branch"
