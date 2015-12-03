from APIGateway import APIGateway

class CircleCiAPIGateway(APIGateway):
  def __init__(self, **args):
    self._host_url = 'https://circleci.com/api/v1'
    self._api = {
      'recent_branch_builds': {
        'path': '/project/{username}/{project}/tree/{branch}',
        'method': 'GET'
      },
      'cancel_build': {
        'path': '/project/{username}/{project}/{build_num}/cancel',
        'method': 'POST'
      },
      'new_build': {
        'path': '/project/{username}/{project}/tree/{branch}',
        'method': 'POST'
      }
    }
    self._common_headers = {
      'Accept': 'application/json'
    }
    self._common_params = {
      'circle-token': args['token']
    }
