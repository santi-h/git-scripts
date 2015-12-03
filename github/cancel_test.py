from CircleCiAPIGateway import CircleCiAPIGateway
from git import Repo
import os

current_branch = Repo(os.getcwd()).active_branch
api = CircleCiAPIGateway(token=os.environ['CIRCLE_TOKEN'])
builds_canceled = 0
for build in api.call('recent_branch_builds', username='bodyshopbidsdotcom', project='snapsheet', branch=current_branch):
  if build['status'] == 'running':
    api.call('cancel_build', username='bodyshopbidsdotcom', project='snapsheet', build_num=build['build_num'])
    builds_canceled += 1

print '{0} builds canceled'.format(builds_canceled)
