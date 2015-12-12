from CircleCiAPIGateway import CircleCiAPIGateway
import Helper
import os

class CircleCiAPIDriver(object):
  def __init__(self):
    self._username, self._project = Helper.owner_and_repo()
    self._api = CircleCiAPIGateway(token=os.environ['CIRCLE_TOKEN'])

  def get_builds(self):
    branch = Helper.current_branch()
    return self._api.call('recent_branch_builds', username=self._username, project=self._project, branch=branch)[0]
