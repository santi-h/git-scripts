import sys
WARNING = u'\U00002622'
CHECK = u'\U00002705'
ERROR = u'\U000026D4'

class StatusPrinter(object):
  def __init__(self, status_len=50):
    self.errors = 0
    self.warnings = 0
    self.last_process_msg_length = 0
    self.status_len = status_len

  def print_process(self, msg):
    sys.stdout.write(msg + ('.' * (self.status_len - len(msg))))
    sys.stdout.flush()

  def print_error(self, msg):
    print u"{0}  {1}".format(ERROR, msg)
    self.errors += 1

  def print_check(self, msg=''):
    print u"{0}  {1}".format(CHECK, msg).strip()

  def print_warning(self, msg):
    print u"{0}  {1}".format(WARNING, msg)
    self.warnings += 1
