from APIGateway import APIGateway

class WrikeAPIGateway(APIGateway):
  def __init__(self, **args):
    self._host_url = 'https://www.wrike.com/api/v3'
    self._api = {
      'refresh_token': {
        'url': 'https://www.wrike.com/oauth2/token',
        'path': '',
        'method': 'POST',
        'params': {
          'grant_type': 'refresh_token'
        }
      },
      'get_token': {
        'url': 'https://www.wrike.com/oauth2/token',
        'path': '',
        'method': 'POST',
        'params': {
          'grant_type': 'authorization_code'
        }
      },
      'get_task': {
        'path': '/tasks/{id}',
        'method': 'GET'
      },
      'id': {
        'path': '/ids',
        'method': 'GET'
      }
    }

    self._common_headers = {}
    if args.get('token') is not None:
      self._common_headers['Authorization'] = 'bearer {0}'.format(args['token'])

    self._common_params = {}

  def update_common_headers(self, data):
    self._common_headers = {
      'Authorization': 'bearer {0}'.format(data['access_token'])
    }
