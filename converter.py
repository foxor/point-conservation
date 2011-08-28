#!/usr/bin/env python2.7

# files contain:
# name1 name2 score1 score2

import math

ITERATIONS = 100

def get_ranking_stats(rankings, name):
  data = list(rankings[name].values())
  average = float(sum(data)) / len(data)
  s = (sum([(float(x) - average) ** 2 for x in data]) / len(data) ** 2) ** 0.5
  return average, s

def compute_certainty(data_point, average, standard_deviation):
  return math.erfc(abs((data_point - average) / (standard_deviation / 2.0))) if standard_deviation else 1

def expected_score(rankings, name, match_number, max_score):
  if not name in rankings:
    rankings[name] = {0:max_score / 2}
    return max_score / 2
  my_rankings = sorted([(x, rankings[name][x]) for x in rankings[name]], key=lambda x: x[0])
  before = [x for x in my_rankings if x[0] < match_number]
  after = [x for x in my_rankings if x[0] > match_number]
  if before and after:
    return (before[-1][1] + after[0][1]) / 2
  elif before:
    return before[-1][1]
  return after[0][1]

def process_match(rankings, match, match_number, max_score):
  #expected_scores = [expected_score(rankings, x, match_number, max_score) for x in match[:2]]
  expected_scores = [overall_score(rankings, x, max_score) for x in match[:2]]
  actual_score = [float(x) for x in match[2:]]
  normalized_score = [(x * max_score) / sum(actual_score) for x in actual_score]
  expected_difference = expected_scores[0] - expected_scores[1]
  normalized_difference = (normalized_score[0] - normalized_score[1]) / 4
  difference_difference = expected_difference - normalized_difference
  test_scores = [expected_scores[0] - difference_difference / 2, expected_scores[1] + difference_difference / 2]
  stats = [get_ranking_stats(rankings, x) for x in match[:2]]
  #import pdb;pdb.set_trace()
  certanty = [compute_certainty(x[0], *x[1]) for x in zip(test_scores, stats)]
  point_delta = difference_difference * (sum(certanty) / len(certanty))
  new_scores = [expected_scores[0] - point_delta / 2, expected_scores[1] + point_delta / 2]
  for n,name in enumerate(match[:2]):
    rankings[name][match_number] = test_scores[n]

def current_score(rankings, name):
  return rankings[name][max(rankings[name].keys())]

def overall_score(rankings, name, max_score = 0):
  if not name in rankings:
    rankings[name] = {0:max_score / 2}
    return max_score / 2
  return sum(rankings[name].values()) / len(rankings[name])

def process_file(fptr):
  matches = [x.strip().split(' ') for x in fptr]
  max_score = 100
  rankings = {}
  for r in xrange(ITERATIONS):
    for n,m in list(enumerate(matches))[::1]:
      process_match(rankings, m, n, max_score)
    for n,m in list(enumerate(matches))[::-1]:
      process_match(rankings, m, n, max_score)
  return rankings

def print_rankings(rankings):
  for n,r in enumerate(sorted([(x, overall_score(rankings, x)) for x in rankings], key=lambda x:-x[1])):
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
