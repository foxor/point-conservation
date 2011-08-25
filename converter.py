#!/usr/bin/env python

# files contain:
# max_score
# name1 name2 score1 score2

ITERATIONS = 100

def expected_score(rankings, name, match_number, max_score):
  if not name in rankings:
    rankings[name] = {0:max_score}
    return max_score
  my_rankings = sorted([(x, rankings[name][x]) for x in rankings[name]], key=lambda x: x[0])
  before = [x for x in my_rankings if x[0] < match_number]
  after = [x for x in my_rankings if x[0] > match_number]
  if before and after:
    return (before[-1][1] + after[0][1]) / 2
  elif before:
    return before[-1][1]
  return after[0][1]

def process_match(rankings, match, match_number, max_score):
  expected_scores = [expected_score(rankings, x, match_number, max_score) for x in match[:2]]
  actual_score = [float(x) for x in match[2:]]
  expected_difference = expected_scores[0] - expected_scores[1]
  actual_difference = actual_score[0] - actual_score[1]
  difference_difference = expected_difference - actual_difference
  new_scores = [expected_scores[0] - difference_difference / 2, expected_scores[1] + difference_difference / 2]
  for n,name in enumerate(match[:2]):
    rankings[name][match_number] = new_scores[n]

def current_score(rankings, name):
  return rankings[name][max(rankings[name].keys())]

def process_file(fptr):
  max_score = float(fptr.readline())
  matches = [x.strip().split(' ') for x in fptr]
  rankings = {}
  for r in xrange(ITERATIONS):
    for n,m in list(enumerate(matches))[::1]:
      process_match(rankings, m, n, max_score)
    for n,m in list(enumerate(matches))[::-1]:
      process_match(rankings, m, n, max_score)
  return rankings

def print_rankings(rankings):
  for n,r in enumerate(sorted([(x, current_score(rankings, x)) for x in rankings], key=lambda x:-x[1])):
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