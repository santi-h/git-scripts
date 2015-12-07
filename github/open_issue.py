import Helper
import re
import webbrowser

branch = Helper.current_branch()
match = re.search('^(\d+)\-', branch)
issue = None
if match is not None:
  owner, repo = Helper.owner_and_repo()
  webbrowser.open('https://github.com/{0}/{1}/issues/{2}'.format(owner, repo, match.group(1)))
else:
  print 'No issue number on branch'
