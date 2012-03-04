<?php
$tournament = "hybrid_DKA";
$path = "input/".$tournament;
$tournaments = array(
  'Draft' => array("draft", $path),
  'Hybrid' => array("draft,sealed", $path),
  'Sealed' => array("sealed", $path)
);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
<title>Isaac James.com</title> 
<link type="text/css" rel="stylesheet" href="/static/menu.css" /> 
<link type="text/css" rel="stylesheet" href="/static/base.css" /> 
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
<script type="text/javascript" src="/static/expando.js"></script>
 
 
</head> 
<body> 
<ul id="nav"> 
  <li class="current"><a href="/">Isaac James</a></li> 
  <li><a href="#">Projects</a> 
    <ul> 
      <li><a href="/baseballbuddy">Baseball Buddy</a></li> 
      <li><a href="/mandelbrot">Mandelbrot</a></li> 
      <li><a href="http://puzzle-blackout.appspot.com/">Puzzle-blackout</a> 
        <ul> 
          <li><p>&nbsp;&nbsp;(click around, don't give up!)</p></li> 
        </ul> 
      </li> 
      <li><a href="/point_conservation">Point Conservation Ranking System</a></li>
    </ul> 
  </li> 
  <li><a href="/resume.pdf">Resume</a></li> 
  <li><a href="/contact">Info</a></li> 
</ul> 
<div id="content">
<h1 style="margin-top: 30px;">Submit Results:</h1>
<p>Please remember to put _sealed or _draft after each player's name</p>
<form action="submit.php" method="GET">
<p><label>Your Name: <input name="name1" type="text" /></label></p>
<p><label>Your Opponent's Name: <input name="name2" type="text" /></label></p>
<p><label>Your Score: <input name="score1" type="text" /></label></p>
<p><label>Your Opponent's score: <input name="score2" type="text" /></label></p>
<p style="display: none"><label>Tournament: <input name="tournament" type="text" value="<?php echo $tournament; ?>" /></label></p>
<input type="submit" />
</form>
<?php foreach ($tournaments as $name => $description) {
  $suffixes = $description[0];
  $files = $description[1];
  ?>
  <div float='left' style="width: <?php echo sprintf("%d", 850.0 / count($tournaments)) ?>px; display: inline-block">
  <h1><?php echo $name ?> Rankings:</h1>
  
  <?php
  system('./converter.py -f '.$files.' -s '.$suffixes);
  ?>
  </div> 
<?php } ?>
<div style="width: <?php echo sprintf("%d", 850.0 / count($tournaments)) ?>px; position: relative; left: <?php echo sprintf("%d", 850.0 / count($tournaments)) ?>px; display: inline-block">
<h1 style="margin-top: 30px;">Previous Matches:</h1>
<?php
#slashes are escaped by php, bash and sed, < and > are escaped by sed
#intent: <br/>
#sed: \<br\/\>
#bash: \<br\\/\>
#php: \<br\\\\/\>
#why does this only with with 5, not 4?
system('cat input/'.$tournament.' | sed s/$/\<br\\\\\/\>/');
?>
</div>
<!-- credit where credit is due --!> 
<div class="clear"></div> 
<p class="footer"><a href="http://www.webdesignerwall.com/tutorials/css3-dropdown-menu/">CSS3 Dropdown Menu</a> <em>by</em> <a href="http://www.webdesignerwall.com">Web Designer Wall</a></p> 
</body> 
</html>
