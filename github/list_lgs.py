from GithubAPIDriver import GithubAPIDriver
import re

driver = GithubAPIDriver()
for comment in driver.get_current_pr_comments():
  match = re.search(r'\bLG\b', comment['body'], flags=re.IGNORECASE)
  if match is not None:
    print "{0}: {1}".format(comment['user']['login'], comment['body'])
