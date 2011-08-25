<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
<title>Isaac James.com</title> 
<link type="text/css" rel="stylesheet" href="/static/menu.css" /> 
<link type="text/css" rel="stylesheet" href="/static/base.css" /> 
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script> 
 
 
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
<h1>Rankings:</h1>
<?php
$fname = "input/".$_GET['tournament'];
if (file_exists($fname)) {
  //echo "appending line to ".$fname."...<br/>";
  $fptr = fopen($fname, 'a');
} else {
  //echo "starting new tournament at ".$fname."...<br/>";
  $fptr = fopen($fname, 'a');
  fwrite($fptr, "2\n");
}
echo "writing line for result...<br/>";
if (!fwrite($fptr, $_GET['name1']." ".$_GET['name2']." ".$_GET["score1"]." ".$_GET['score2']."\n")) {
  //echo "write failed<br/>";
}
fclose($fptr);
//echo "shelling out to converter.py for new rankings...<br/>";
system('./converter.py input/'.$_GET['tournament']);
?>
<h2>Thanks!</h2>
</div> 
<!-- credit where credit is due --!> 
<div class="clear"></div> 
<p class="footer"><a href="http://www.webdesignerwall.com/tutorials/css3-dropdown-menu/">CSS3 Dropdown Menu</a> <em>by</em> <a href="http://www.webdesignerwall.com">Web Designer Wall</a></p> 
</body> 
</html>
