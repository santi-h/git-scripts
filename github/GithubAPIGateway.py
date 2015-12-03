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
        'method': 'GET'
      },
      'user': {
        'path': '/user',
        'method': 'GET'
      },
      'create_issue': {
        'path': '/repos/{owner}/{repo}/issues',
        'method': 'POST'
      }
    }
    self._common_headers = {
      'Authorization': 'token {0}'.format(args['token'])
    }
    self._common_params = {}
