from GithubAPIDriver import GithubAPIDriver
from GithubLGModule import get_lg_data
from CircleCiAPIDriver import CircleCiAPIDriver
from StatusPrinter import StatusPrinter
import Helper
import sys
import re

circle_driver = CircleCiAPIDriver()
github_driver = GithubAPIDriver()
printer = StatusPrinter()

###################################################################################################
# MAKE SURE LOCAL AND REMOTE BRANCH ARE THE SAME
###################################################################################################
printer.print_process('Checking for differences with local branch')
commits = github_driver.get_pr_commits()
if len(commits) <= 0:
  printer.print_error("No commits on the pr. Suggestion: push any changes")
else:
  pr_sha = commits[-1]['sha']
  local_sha = Helper.local_sha()
  if pr_sha != local_sha:
    branch = Helper.current_branch()
    printer.print_warning("The commit on the pr is different than local. Suggestion: (git push -f origin {0}) or (git pull origin {0})".format(branch))
  else:
    printer.print_check()

###################################################################################################
# MAKE SURE MASTER LOCAL AND REMOTE ARE THE SAME
###################################################################################################
printer.print_process('Checking for differences with local master')
if Helper.local_sha('master') != Helper.origin_sha('master'):
  printer.print_warning("Remote master is different than local master. Suggestion: (git checkout master && git pull origin master)")
else:
  printer.print_check()

###################################################################################################
# CHECK FOR UNBROUGHT CHANGES FROM MASTER
###################################################################################################
printer.print_process('Checking for unbrought in changes in master')
if not Helper.branch_contains('master'):
  printer.print_warning("There are unbrought changes in master. Suggestion: (git rebase master)")
else:
  printer.print_check()

###################################################################################################
# CHECK FOR CIRCLECI TESTS
###################################################################################################
printer.print_process('Checking CircleCi tests status')
passed = False
for build in circle_driver.get_builds():
  if build['vcs_revision'] == Helper.local_sha() and build['outcome'] == 'success':
    passed = True
    break
if passed:
  printer.print_check()
else:
  printer.print_error("Tests have not yet passed")

###################################################################################################
# CHECK FOR LGS
###################################################################################################
printer.print_process('Checking for LGs and unaddressed comments')
lg_data = get_lg_data(github_driver)
if lg_data['lgs_count'] < 2:
  printer.print_error('{0} LGs found. Suggestion: run git_list_lgs for a detail description'.format(lg_data['lgs_count']))
elif lg_data['has_unaddressed_comments']:
  printer.print_error('Unnaddressed comments found. Suggestion: run git_list_lgs for a detailed description')
else:
  printer.print_check()

sys.exit(printer.errors)
