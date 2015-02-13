#!/usr/bin/python

import sys, re

args = sys.argv

_RE_WORD_SPLIT = r"[^A-Za-z\']"

_WORDS_DICT = dict()
_WORDS_COUNT = 0

for infile in args[1:]:
  with open(infile, 'r') as fp:
    for line in fp:
      words = re.split(_RE_WORD_SPLIT, line)
      for word in words:
        if not word:
          continue
        _WORDS_COUNT += 1
        word = word.lower()
        if word in _WORDS_DICT:
          _WORDS_DICT[word] = _WORDS_DICT[word] + 1
        else:
          _WORDS_DICT[word] = 1

for k,v in sorted(_WORDS_DICT.items(), key=lambda p:p[1]):
  print "Word: '%s' appear %d times" % (k, v)

print "There are %d different words in the article" % len(_WORDS_DICT)
print "There are %d words in total in the article" % _WORDS_COUNT
