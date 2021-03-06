import re
import requests
import json
import sys

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
      result = requests.post(self.api_full_path(api, **args), headers=self._common_headers, params=params, json=args.get('data'))
    elif self.method(api) == 'PUT':
      result = requests.put(self.api_full_path(api, **args), headers=self._common_headers, params=params, json=args.get('data'))

    ret = None
    status = None
    if result is not None:
      ret = json.loads(result.text)
      status = result.status_code

    if status is not None and self._api[api].get('valid_status') is not None and status not in self._api[api]['valid_status']:
      print "Warning - Status: {0}".format(status)
      print "Warning - Response: {0}".format(ret)

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
