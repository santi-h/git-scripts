from GithubAPIDriver import GithubAPIDriver
from GithubLGModule import get_lg_data
import re
from datetime import datetime

lg_data = get_lg_data()
lgs_count = lg_data.pop('lgs_count')
lg_data.pop('has_unaddressed_comments', None)
for user, data in lg_data.iteritems():
  if len(data['unaddressed_comments']) > 0:
    if data['lgcomment'] is not None:
      print "{0} LGd at some point but has the following unaddressed comments:".format(user)
    else:
      print "{0} has the following unaddressed comments:".format(user)

    for unaddressed_comment in data['unaddressed_comments']:
      print '\t> ({0}) {1}'.format(unaddressed_comment['updated_at_datetime'], unaddressed_comment['html_url'])
      print '\t{0}'.format(unaddressed_comment['body'])
    print ''
  else:
    if data['lgcomment'] is not None:
      # All user's comments have been addressed and he has LGd, +1!
      print "+1 {0}: {1}".format(user, data['lgcomment'])
      print ''
    else:
      # User has no unaddressed comments but he has not yet LGd
      pass

print "{0} LGs".format(lgs_count)
