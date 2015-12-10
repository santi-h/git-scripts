from GithubAPIDriver import GithubAPIDriver
import re
import webbrowser

driver = GithubAPIDriver()
issue = driver.get_current_issue()

match = re.search('(https://www\.wrike\.com/(?:open\.htm\?)id=[\d\w]+)', issue.get('body') or '')
if match is not None:
  print match.group(1)
  webbrowser.open(match.group(1))
else:
  print 'No wrike task address found'
