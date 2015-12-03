from CircleCiAPIGateway import CircleCiAPIGateway
from git import Repo
import os

current_branch = Repo(os.getcwd()).active_branch
api = CircleCiAPIGateway(token=os.environ['CIRCLE_TOKEN'])
result = api.call('new_build', username='bodyshopbidsdotcom', project='snapsheet', branch=current_branch)
if result.get('build_num') is not None:
  print 'Build {0} started'.format(result['build_num'])
else:
  if result.get('message') is not None:
    print result['message']
  else:
    print result
