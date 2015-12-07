from CircleCiAPIGateway import CircleCiAPIGateway
from git import Repo
import os
import Helper

current_branch = Repo(os.getcwd()).active_branch
api = CircleCiAPIGateway(token=os.environ['CIRCLE_TOKEN'])
owner, repo = Helper.owner_and_repo()
result = api.call('new_build', username=owner, project=repo, branch=current_branch)[0]
if result.get('build_url') is not None:
  print result['build_url']
else:
  if result.get('message') is not None:
    print result['message']
  else:
    print result
