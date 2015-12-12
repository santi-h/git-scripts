from GithubAPIGateway import GithubAPIGateway
import Helper
import os
from datetime import datetime
from operator import itemgetter
import copy

class GithubAPIDriver(object):
  def __init__(self):
    self._owner, self._repo = Helper.owner_and_repo()
    self._api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
    self._cache = {}

  def get_open_pr(self):
    ret = self._cache.get('pr')
    if ret is not None:
      return ret

    branch = str(Helper.current_branch())
    prs = self._api.call('list_pr', owner=self._owner, repo=self._repo, data={
      'head': branch
    })[0]

    for pr in prs:
      if pr['head']['ref'] == branch:
        self._cache['pr'] = pr
        return pr

    return None

  def get_current_issue(self):
    ret = self._cache.get('issue')
    if ret is not None:
      return ret

    issue_number = Helper.issue_number_from_branch()
    ret = self._api.call('list_issue', owner=self._owner, repo=self._repo, number=issue_number)[0]

    self._cache['issue'] = ret
    return ret

  def get_pr_comments(self):
    ret = self._cache.get('pr_comments')
    if ret is not None:
      return ret

    pr = self.get_open_pr()
    ret = None
    if pr is not None:
      ret = self._api.call('list_issue_comments', owner=self._owner, repo=self._repo, number=pr['number'])[0]
    else:
      ret = []

    self._cache['pr_comments'] = ret
    return ret

  def get_pr_commits(self):
    ret = self._cache.get('pr_commits')
    if ret is not None:
      return ret

    pr = self.get_open_pr()
    if pr is not None:
      ret = self._api.call('list_pr_commits', owner=self._owner, repo=self._repo, number=pr['number'])[0]
    else:
      ret = []

    self._cache['pr_commits'] = ret
    return ret

  def get_user(self):
    ret = self._cache.get('user')
    if ret is not None:
      return ret

    ret = self._api.call('user')[0]

    self._cache['user'] = ret
    return ret

  def get_pr_review_comments(self):
    ret = self._cache.get('pr_review_comments')
    if ret is not None:
      return ret

    pr = self.get_open_pr()
    if pr is not None:
      ret = self._api.call('list_pr_review_comments', owner=self._owner, repo=self._repo, number=pr['number'])[0]
    else:
      ret = []

    self._cache['pr_review_comments'] = ret
    return ret

  def get_pr_and_review_comments(self):
    review_comments = self.get_pr_review_comments()
    pr_comments = self.get_pr_comments()
    comments = {}
    for comment_original in (review_comments + pr_comments):
      comment = copy.deepcopy(comment_original)
      user = comment['user']['login']
      if comments.get(user) is None:
        comments[user] = []

      comment['updated_at_datetime'] = datetime.strptime(comment['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
      comments[user].append(comment)

    for user, comments_array in comments.iteritems():
      comments_array.sort(key=itemgetter('updated_at_datetime'))

    return comments
