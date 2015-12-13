from WrikeAPIGateway import WrikeAPIGateway

class WrikeAPIDriver(object):
  def __init__(self):
    self._api = WrikeAPIGateway()
    self._cache = {}

  def get_task(self, task_id):
    response = self._api.call('get_task', id=task_id)[0]
    if response.get('data') is not None and len(response['data']) > 0:
      return response['data'][0]
    else:
      return None

  def complete_task(self, task_id):
    response = self._api.call('modify_task', id=task_id, params={
      'status': 'Completed'
    })[0]
    if response.get('data') is not None and len(response['data']) > 0:
      return response['data'][0]
    else:
      return None
