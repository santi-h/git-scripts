from GithubAPIDriver import GithubAPIDriver
from WrikeAPIDriver import WrikeAPIDriver
from StatusPrinter import StatusPrinter
import Helper
import re
import sys

github_driver = GithubAPIDriver()
wrike_driver = WrikeAPIDriver()
printer = StatusPrinter(70)

###################################################################################################
# 'CLICK' MERGE BUTTON
###################################################################################################
printer.print_process('Triggering "Merge pull request" button actions')
result = github_driver.merge_pr()
if result is not None:
  if result.get('merged') is not None and result['merged'] == True:
    printer.print_check()
  else:
    if result.get('message') is not None:
      printer.print_error(result['message'])
    else:
      printer.print_error('Could not perform merge')
    sys.exit(-1)
else:
  printer.print_error('Could not find open PR')
  sys.exit(-1)

###################################################################################################
# CLOSE WRIKE TASK
###################################################################################################
printer.print_process('Finding issue')
issue = github_driver.get_current_issue()
if issue.get('number') is None:
  printer.print_warning('No issue found')
else:
  printer.print_check()

  printer.print_process('Finding wrike task')
  matches = re.findall('(https://www\.wrike\.com/(?:open\.htm\?)id=([\d\w]+))', issue.get('body') or '')
  if len(matches) <= 0:
    printer.print_warning('No wrike tasks found')
  else:
    printer.print_check()
    for task_tuple in matches:
      printer.print_process('Completing task {0}'.format(task_tuple[0]))
      task = wrike_driver.complete_task(task_tuple[1])
      if task is not None and task.get('status') is not None and task['status'] == 'Completed':
        printer.print_check()
      else:
        printer.print_warning('Task could not be changed to completed')

###################################################################################################
# REMOVE REMOTE BRANCH
###################################################################################################
printer.print_process('Removing remote branch')
if Helper.delete_origin_branch():
  printer.print_check()
else:
  owner, repo = Helper.owner_and_repo()
  printer.print_warning('Could not remove it. Visit https://github.com/{0}/{1}/branches to remove manually'.format(owner, repo))
