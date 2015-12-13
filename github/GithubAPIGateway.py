from APIGateway import APIGateway

class GithubAPIGateway(APIGateway):
  def __init__(self, **args):
    self._host_url = 'https://api.github.com'
    self._api = {
      'list_issues': {
        'path': '/orgs/{org}/issues',
        'method': 'GET'
      },
      'list_issue': {
        'path': '/repos/{owner}/{repo}/issues/{number}',
        'method': 'GET',
        'valid_status': [200, 404]
      },
      'user': {
        'path': '/user',
        'method': 'GET',
        'valid_status': [200]
      },
      'create_issue': {
        'path': '/repos/{owner}/{repo}/issues',
        'method': 'POST'
      },
      'create_pr': {
        'path': '/repos/{owner}/{repo}/pulls',
        'method': 'POST',
        'valid_status': [201]
      },
      'list_pr': {
        'path': '/repos/{owner}/{repo}/pulls',
        'method': 'GET',
        'valid_status': [200]
      },
      'list_pr_review_comments': {
        'path': '/repos/{owner}/{repo}/pulls/{number}/comments',
        'method': 'GET',
        'valid_status': [200]
      },
      'list_issue_comments': {
        'path': '/repos/{owner}/{repo}/issues/{number}/comments',
        'method': 'GET',
        'valid_status': [200]
      },
      'list_pr_commits': {
        'path': '/repos/{owner}/{repo}/pulls/{number}/commits',
        'method': 'GET',
        'valid_status': [200]
      },
      'merge_pr': {
        'path': '/repos/{owner}/{repo}/pulls/{number}/merge',
        'method': 'PUT',
        'valid_status': [200]
      }
    }
    self._common_headers = {
      'Authorization': 'token {0}'.format(args['token'])
    }
    self._common_params = {}
