#!/usr/bin/env python2.7

# files contain:
# name1 name2 score1 score2

ITERATIONS = 20
START_SCORE = 5

def score(rankings, name):
  if not name in rankings:
    rankings[name] = START_SCORE
    return START_SCORE
  return rankings[name]

def process_match(rankings, match, match_number, season):
  names = match[:2]
  player_rankings = [score(rankings, x) for x in names]
  pool = sum(player_rankings)
  match_scores = [float(x) for x in match[2:]]
  difference = match_scores[0] - match_scores[1]
  new_scores = [pool / 2 + difference / 2, pool / 2 - difference / 2]
  if any([match_scores[x] == 0 and player_rankings[x] < new_scores[x] for x in [0, 1]]):
    #print "Winner protection engaged for match: %s" % match
    new_scores = player_rankings
    
  for n,name in enumerate(match[:2]):
    season[name] = season.get(name, {})
    season[name][match_number] = new_scores[n]

def process_file(fptr):
  matches = [x.strip().split(' ') for x in fptr]
  rankings = {}
  _continue = True
  while _continue:
    _continue = False
    season = {}
    for n,m in list(enumerate(matches))[::1]:
      process_match(rankings, m, n, season)
    for player in season:
      new_rank = sum(season[player].values()) / len(season[player])
      _continue |= abs(score(rankings, player) - new_rank) > 0.0005
      rankings[player] = new_rank

    rankings = dict([(x, sum(season[x].values()) / len(season[x])) for x in season])
  return rankings

def print_rankings(rankings):
  for n,r in enumerate(sorted([(x, rankings[x]) for x in rankings], key=lambda x:-x[1])):
    print "<p>%d: %s with %.2f points</p>" %(n+1, r[0], r[1])

if __name__ == '__main__':
  #print "trying to open file...<br/>"
  import sys
  try:
    fptr = open(sys.argv[1], 'r')
    rankings = process_file(fptr)
    if rankings:
      print_rankings(rankings)
    else:
      print "<p>Nobody has played yet</p>"
  except Exception, e:
    import sys
    print sys.exc_info()
