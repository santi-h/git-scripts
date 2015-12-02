import re
import requests
import json

class APIGateway(object):
  def call(self, api, **args):
    if self.method(api) == 'GET':
      result = requests.get(self.api_full_path(api, **args), headers=self._common_headers)
      return json.loads(result.text)

    return None

  def apis(self):
    return self._api.keys()

  def params(self, api):
    return re.findall('\{([^\}]*)\}', self._api[api]['path'])

  def method(self, api):
    return self._api[api]['method']

  def api_full_path(self, api, **args):
    return ''.join([
      self._host_url,
      self._api[api]['path'].format(**args)
    ])
