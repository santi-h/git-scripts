from APIGateway import APIGateway
import os
import json
import webbrowser
import SocketServer
import socket
import BaseHTTPServer
import re
import Helper
import threading

class WrikeCodeServer(BaseHTTPServer.BaseHTTPRequestHandler):
  def __init__(self, *args):
    self.code = None
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)

  def do_GET(self):
    match = re.search('code=([\w|\-]+)', self.path)
    if match is not None:
      self.server.authentication_code = match.group(1)
      while self.server.redirect is None: pass
      self.send_response(301)
      self.send_header('Location', self.server.redirect)
      self.end_headers()
    else:
      self.server.authentication_code = 0
      self.send_response(406)
      self.end_headers()

class QuickSocketServer(SocketServer.TCPServer):
  def __init__(self):
    self.authentication_code = None
    self.redirect = None
    SocketServer.TCPServer.__init__(self, ("", 19877), WrikeCodeServer)

  def server_bind(self):
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind(self.server_address)

class ServerThread(threading.Thread):
  def __init__(self, httpd, **args):
    self._httpd = httpd
    threading.Thread.__init__(self, **args)

  def run(self):
    self._httpd.handle_request()

class WrikeAPIGateway(APIGateway):
  def __init__(self, redirect=None):
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
        },
        'valid_status': [200]
      },
      'get_task': {
        'path': '/tasks/{id}',
        'method': 'GET',
        'translate': [
          {
            'type': 'ApiV2Task',
            'params': ['id']
          }
        ]
      },
      'id': {
        'path': '/ids',
        'method': 'GET'
      },
      'create_comment_in_task_v3': {
        'path': '/tasks/{idv3}/comments',
        'method': 'POST',
        'valid_status': [200]
      }
    }

    self._common_headers = {}
    self._common_params = {}
    self._auth_info = {}
    self._redirect = redirect
    self._httpd = None
    self._serverthread = None

  def update_common_headers(self, data):
    self._common_headers = {
      'Authorization': 'bearer {0}'.format(data['access_token'])
    }

  def redirect(self, redirect="http://www.google.com"):
    if redirect is not None:
      if self._httpd is not None:
        self._httpd.redirect = redirect
        self._httpd = None

      if self._serverthread is not None:
        self._serverthread.join()
        self._serverthread = None

  def call(self, api, **args):
    self._authenticate_client()
    return self._call(api, **args)

  def _call(self, api, **args):
    if self._api[api].get('translate') is not None:
      for translate in self._api[api]['translate']:
        for param in translate['params']:
          args[param] = self._call('id', params={
            'ids': '[{0}]'.format(args[param]),
            'type': translate['type']
          })[0]['data'][0]['id']

    result, status = super(WrikeAPIGateway, self).call(api, **args)

    if status == 401 and result['error'] == 'not_authorized':
      self._refresh_client_authentication()
      result, status = super(WrikeAPIGateway, self).call(api, **args)

    return result, status

  def _refresh_client_authentication(self):
    auth_info = super(WrikeAPIGateway, self).call('refresh_token', params={
      'client_id': os.environ['WRIKE_CLIENT_ID'],
      'client_secret': os.environ['WRIKE_CLIENT_SECRET'],
      'refresh_token': self._auth_info['refresh_token']
    })[0]

    with open(self._get_auth_file_filepath(), 'w') as outfile:
      json.dump(auth_info, outfile)

    self._auth_info = auth_info
    self.update_common_headers(auth_info)

  def _authenticate_client(self):
    auth_info = self._get_auth_info()
    if auth_info is None:
      auth_info = self._create_auth_info()

    self._auth_info = auth_info
    self.update_common_headers(auth_info)

  def _create_auth_info(self):
    webbrowser.open('https://www.wrike.com/oauth2/authorize?client_id={0}&response_type=code'.format(os.environ['WRIKE_CLIENT_ID']))
    self._httpd = QuickSocketServer()
    self._serverthread = ServerThread(self._httpd)
    self._serverthread.start()
    while self._httpd.authentication_code is None: pass
    authentication_code = self._httpd.authentication_code
    if self._redirect is not None:
      self.redirect(self._redirect)

    owner, repo = Helper.owner_and_repo()
    auth_info = super(WrikeAPIGateway, self).call('get_token', params={
      'client_id': os.environ['WRIKE_CLIENT_ID'],
      'client_secret': os.environ['WRIKE_CLIENT_SECRET'],
      'code': authentication_code
    })[0]
    with open(self._get_auth_file_filepath(), 'w') as outfile:
      json.dump(auth_info, outfile)

    return auth_info

  def _get_auth_info(self):
    filepath = self._get_auth_file_filepath()
    data = None
    if os.path.isfile(filepath):
      with open(filepath) as data_file:
        data = json.load(data_file)

    return data

  def _get_auth_file_filepath(self):
    data_file_dirpath = os.path.dirname(os.path.realpath(__file__))
    data_file_filename = os.path.splitext(os.path.basename(__file__))[0] + '.json'
    return data_file_dirpath + '/' + data_file_filename
