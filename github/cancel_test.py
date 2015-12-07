from CircleCiAPIGateway import CircleCiAPIGateway
from git import Repo
import os
import Helper

current_branch = Repo(os.getcwd()).active_branch
api = CircleCiAPIGateway(token=os.environ['CIRCLE_TOKEN'])
builds_canceled = 0
owner, repo = Helper.owner_and_repo()

for build in api.call('recent_branch_builds', username=owner, project=repo, branch=current_branch)[0]:
  if build['status'] in ['running', 'not_running', 'queued', 'scheduled']:
    api.call('cancel_build', username=owner, project=repo, build_num=build['build_num'])
    builds_canceled += 1

print '{0} builds canceled'.format(builds_canceled)
