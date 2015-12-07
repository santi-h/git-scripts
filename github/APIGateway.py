import re
import requests
import json

class APIGateway(object):
  def call(self, api, **args):
    params = {}
    params.update(self._common_params)
    if self._api[api].get('params') is not None:
      params.update(self._api[api]['params'])
    if args.get('params') is not None:
      params.update(args['params'])

    result = None
    if self.method(api) == 'GET':
      result = requests.get(self.api_full_path(api, **args), headers=self._common_headers, params=params)
    elif self.method(api) == 'POST':
      result = requests.post(self.api_full_path(api, **args), headers=self._common_headers, json=args.get('data'), params=params)

    ret = None
    status = None
    if result is not None:
      ret = json.loads(result.text)
      status = result.status_code

    return ret, status

  def apis(self):
    return self._api.keys()

  def params(self, api):
    return re.findall('\{([^\}]*)\}', self._api[api]['path'])

  def method(self, api):
    return self._api[api]['method']

  def api_full_path(self, api, **args):
    url = self._host_url
    if self._api[api].get('url') is not None:
      url = self._api[api]['url']
    return ''.join([
      url,
      self._api[api]['path'].format(**args)
    ])
