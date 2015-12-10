from GithubAPIGateway import GithubAPIGateway
import Helper
import os

class GithubAPIDriver(object):
  def __init__(self):
    self._owner, self._repo = Helper.owner_and_repo()
    self._api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])

  def get_open_pr(self):
    branch = str(Helper.current_branch())
    prs = self._api.call('list_pr', owner=self._owner, repo=self._repo, data={
      'head': branch
    })[0]

    for pr in prs:
      if pr['head']['ref'] == branch:
        return pr

    return None

  def get_current_issue(self):
    issue_number = Helper.issue_number_from_branch()
    ret = self._api.call('list_issue', owner=self._owner, repo=self._repo, number=issue_number)[0]
    return ret
