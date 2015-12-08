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
        'valid_status': [200]
      },
      'user': {
        'path': '/user',
        'method': 'GET'
      },
      'create_issue': {
        'path': '/repos/{owner}/{repo}/issues',
        'method': 'POST'
      },
      'create_pr': {
        'path': '/repos/{owner}/{repo}/pulls',
        'method': 'POST',
        'valid_status': [201]
      }
    }
    self._common_headers = {
      'Authorization': 'token {0}'.format(args['token'])
    }
    self._common_params = {}
