#!/usr/bin/python
import random

_default_string = '1234567890abcedfghijklmnopqrstuvwxyz'

def _random_str(length):
  ran_str = ''
  ran_int = random.randint(1, length)
  default_len = len(_default_string)
  for x in xrange(ran_int):
    a = random.randint(1, default_len-1)
    ran_str += _default_string[a]
  return ran_str


def _confusion_code(length, r_str):
  r_str = r_str.lower()
  r_len = len(r_str)
  default_len = len(_default_string)
  ran_str = ''
  for x in xrange(length):
    a = random.randint(0, r_len-1)
    a = ord(r_str[a])
    a = random.randint(0, a)
    a = a % default_len if a >= default_len else a
    ran_str += _default_string[a]
  return ran_str.upper()


class PromoCodeGenerator(object):

  _codes = []

  def __init__(self, code_num, code_len=15, comments=None):
    self._code_len = code_len
    self._code_num = code_num
    self._r_str = comments

  def _test_code(self, code):
    return code in self._codes

  def _gen_promo_code(self):
    r_str = self._r_str or _random_str(self._code_len)
    code = _confusion_code(self._code_len, r_str)
    return code
  
  def get_codes(self):
    for x in xrange(self._code_num):
      code = self._gen_promo_code()
      while self._test_code(code):
        code = self._gen_promo_code()
      self._codes.append(code)
    return self._codes
    
if __name__ == '__main__':
  pcg = PromoCodeGenerator(50, 20, 'For old customer')
  codes = pcg.get_codes()
  import re
  _PRETTY_CODE_RE = re.compile(r'(\w{5})')
  for x in codes:
    print re.sub(_PRETTY_CODE_RE, r'\1-', x)[:-1]











