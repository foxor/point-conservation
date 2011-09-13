<?php
$fname = "input/".$_GET['tournament'];
if (file_exists($fname)) {
  //echo "appending line to ".$fname."...<br/>";
  $fptr = fopen($fname, 'a');
} else {
  //echo "starting new tournament at ".$fname."...<br/>";
  system('touch '.$fname);
  $fptr = fopen($fname, 'a');
  fwrite($fptr, "2\n");
}
echo "writing line for result...<br/>";
if (!fwrite($fptr, $_GET['name1']." ".$_GET['name2']." ".$_GET["score1"]." ".$_GET['score2']."\n")) {
  echo "write failed".$fname."<br/>";
}
fclose($fptr);
//echo "shelling out to converter.py for new rankings...<br/>";
system('./converter.py input/'.$_GET['tournament']);
header( 'Location: /point_conservation');
?>
