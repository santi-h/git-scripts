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
branch = Helper.current_branch()
prs = api.call('list_pr', owner=owner, repo=repo, data={
  'head': owner + ':' + str(branch)
})[0]

if len(prs) > 0:
  url = prs[0]['html_url']
  print url
  if args.open:
    webbrowser.open(url)
else:
  print "No PRs on this branch"
