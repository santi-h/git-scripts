from WrikeAPIGateway import WrikeAPIGateway
from GithubAPIGateway import GithubAPIGateway
from git import Repo
import os
import sys
import re
import SocketServer
import BaseHTTPServer
import socket
import json
import webbrowser

class QuickSocketServer(SocketServer.TCPServer):
  def server_bind(self):
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind(self.server_address)

class WrikeCodeServer(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    code = re.search('code=([\w|\-]+)', self.path).group(1)
    data = create_data_file(code)
    issue_url = do_it(data)
    self.send_response(301)
    self.send_header('Location', issue_url)
    self.end_headers()

def get_data_file_filepath():
  data_file_dirpath = os.path.dirname(os.path.realpath(__file__))
  data_file_filename = os.path.splitext(os.path.basename(__file__))[0] + '.json'
  return data_file_dirpath + '/' + data_file_filename

# returns a json with the info in the data file or None if there's non data file
def get_data_file():
  filepath = get_data_file_filepath()
  data = None
  if os.path.isfile(filepath):
    with open(filepath) as data_file:
      data = json.load(data_file)

  return data

# makes the api call to wrike to get the authentication code and returns it, or None if it failed
def get_authentication_code_and_do_it():
  webbrowser.open('https://www.wrike.com/oauth2/authorize?client_id={0}&response_type=code'.format(os.environ['WRIKE_CLIENT_ID']))
  httpd = QuickSocketServer(("", 19877), WrikeCodeServer)
  httpd.handle_request()

# creates the data info file by using the authentication_code and requesting a token
# returns the json info
def create_data_file(authentication_code):
  api = WrikeAPIGateway()
  data = api.call('get_token', owner='bodyshopbidsdotcom', repo='snapsheet', params={
    'client_id': os.environ['WRIKE_CLIENT_ID'],
    'client_secret': os.environ['WRIKE_CLIENT_SECRET'],
    'code': authentication_code
  })
  with open(get_data_file_filepath(), 'w') as outfile:
    json.dump(data, outfile)

  return data

def create_issue(task):
  api = GithubAPIGateway(token=os.environ['GITHUB_TOKEN'])
  username = api.call('user')['login']
  body = task['permalink'] + '\n\n' + task['description']
  issue = api.call('create_issue', owner='bodyshopbidsdotcom', repo='snapsheet', data={
    'title': task['title'],
    'assignee': username,
    'body': body
  })
  return issue

def create_branch(issue):
  branch_name = str(issue['number']) + '-' + re.sub('[^\w\d]+', '-', issue['title'].strip().lower())[0:30].strip('-')
  git = Repo(os.getcwd()).git
  git.checkout('HEAD', b=branch_name)
  return branch_name

def api_wrapper(api, auth_data, method, **args):
  result = api.call(method, **args)
  if result['_status_code'] == 401 and result['error'] == 'not_authorized':
    data = api.call('refresh_token', params={
      'client_id': os.environ['WRIKE_CLIENT_ID'],
      'client_secret': os.environ['WRIKE_CLIENT_SECRET'],
      'refresh_token': auth_data['refresh_token']
    })

    with open(get_data_file_filepath(), 'w') as outfile:
        json.dump(data, outfile)

    api.update_common_headers(data)
    result = api.call(method, **args)

  return result

def do_it(auth_data):
  api = WrikeAPIGateway(token=auth_data['access_token'])
  result = api_wrapper(api, auth_data, 'id', params= {
    'ids': '[{0}]'.format(sys.argv[1]),
    'type': 'ApiV2Task'
  })
  idv3 = result['data'][0]['id']
  task = api_wrapper(api, auth_data, 'get_task', id=idv3)['data'][0]
  issue = create_issue(task)
  create_branch(issue)
  print issue['html_url']
  return issue['html_url']

data = get_data_file();
if data is None:
  get_authentication_code_and_do_it()
else:
  do_it(data)

