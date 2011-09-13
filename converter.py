#!/usr/bin/env python2.7

# files contain:
# name1 name2 score1 score2

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
  return rankings, season, matches

def won(name, match):
  return ((name == match[0]) == (match[2] > match[3]))

def other_name(name, match):
  return match[0] if name == match[1] else match[1]

def more_info(name, rank, info, matches):
  r = ["""<div class="emphasis"><h4>Match History:</h3>"""]
  wins = 0
  for player_number, match_number in enumerate(sorted(info)):
    match = matches[match_number]
    r.append("""<p>%d: %s vs %s %s - %s &mdash; <span style="color:%s">%+.2f points</span></p>""" % (player_number, "won" if won(name, match) else "lost", other_name(name, match), match[2], match[3], "green" if info[match_number] > rank else "red", info[match_number] - rank))
    wins += 1 if won(name, match) else 0
  r.append("<h4>Record: %d and %d (%.2f%%)</h4>" % (wins, len(info.keys()) - wins, 100.0 * wins / len(info.keys())))
  r.append("</div>")
  return ''.join(r)

def print_rankings(rankings, season, matches):
  for n,r in enumerate(sorted([(x, rankings[x], more_info(x, rankings[x], season[x], matches)) for x in rankings], key=lambda x:-x[1])):
    print "<div class='swap'>%d: %s with %.2f points [<a href='#' class='swap_button'>+</a>]<div class='closed'>%s</div></div><div style='clear:both'></div>" %(n+1, r[0], r[1], r[2])

if __name__ == '__main__':
  #print "trying to open file...<br/>"
  import sys
  try:
    fptr = open(sys.argv[1], 'r')
    rankings, season, matches = process_file(fptr)
    if rankings:
      print_rankings(rankings, season, matches)
    else:
      print "<p>Nobody has played yet</p>"
  except Exception, e:
    import sys
    print sys.exc_info()
