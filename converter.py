#!/usr/bin/env python2.7

# files contain:
# name1 name2 score1 score2

import math

ITERATIONS = 100
START_SCORE = 5

def score(rankings, name, season):
  if not name in rankings:
    rankings[name] = START_SCORE
    return START_SCORE
  return rankings[name]

def process_match(rankings, match, match_number, season):
  pool = sum([score(rankings, x, season) for x in match[:2]])
  actual_score = [float(x) for x in match[2:]]
  difference = actual_score[0] - actual_score[1]
  new_scores = [pool / 2 + difference / 2, pool / 2 - difference / 2]
  #import pdb;pdb.set_trace()
  for n,name in enumerate(match[:2]):
    season[name] = season.get(name, {})
    season[name][match_number] = new_scores[n]

def process_file(fptr):
  matches = [x.strip().split(' ') for x in fptr]
  rankings = {}
  for r in xrange(ITERATIONS):
    season = {}
    for n,m in list(enumerate(matches))[::1]:
      process_match(rankings, m, n, season)
    #import pdb;pdb.set_trace()
    rankings = dict([(x, sum(season[x].values()) / len(season[x])) for x in season])
  return rankings

def print_rankings(rankings):
  for n,r in enumerate(sorted([(x, rankings[x]) for x in rankings], key=lambda x:-x[1])):
    print "<p>%d: %s with %.2f points</p>" %(n+1, r[0], r[1])

if __name__ == '__main__':
  print "trying to open file...<br/>"
  try:
    import sys
    fptr = open(sys.argv[1], 'r')
    print_rankings(process_file(fptr))
  except Exception, e:
    import sys
    print sys.exc_info()
