from GithubAPIDriver import GithubAPIDriver
import re
from datetime import datetime

def get_ids_addressed(by_user, all_comments):
  ret = set()
  for current_user_comment in all_comments.get(by_user) or []:
    match = re.search(r'discussion_r(\d+)|issuecomment-(\d+)', current_user_comment['body'])
    if match is not None:
      ret.add(match.group(1) or match.group(2))
  return ret

def get_lg_data(driver=GithubAPIDriver()):
  current_user = driver.get_user()['login']
  all_comments = driver.get_pr_and_review_comments()
  comment_ids_addressed = get_ids_addressed(current_user, all_comments)
  all_comments.pop(current_user, None)
  ret = {}
  ret['lgs_count'] = 0
  ret['has_unaddressed_comments'] = False
  for comments_user, comments in all_comments.iteritems():
    unaddressed_comments = []
    lgd = False
    lgcomment = None
    for comment in reversed(comments):
      match = re.search(r'\bLG\b', comment['body'], flags=re.IGNORECASE)
      if match is not None:
        lgcomment = comment['body']
        if len(unaddressed_comments) <= 0:
          ret['lgs_count'] += 1
        break
      else:
        if str(comment['id']) not in comment_ids_addressed:
          unaddressed_comments.append(comment)

    if len(unaddressed_comments) > 0:
      ret['has_unaddressed_comments'] = True

    ret[comments_user] = {
      'unaddressed_comments': unaddressed_comments,
      'lgcomment': lgcomment
    }

  return ret
