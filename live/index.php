<HTML> 
<head>
<Title>Subtitle Files</title>
<link rel="stylesheet" type="text/css" href="white.css">
</head>
<Body> 
<div id="columns">

<h1>Subtitles Available</h1>
This is the list of subtitles currently available to view:

<table>
<tr><td>
Program
</td>
<td>
Language</td>
<?php 
$files1 = scandir(".");
//print_r($files1);
foreach ($files1 as $file){
	if (strpos($file,'html') !== false){
		$split_string=explode("_",$file);
		echo "<tr><td><a href=\"".$file;
		$language=str_replace(".html","",$split_string[1]);
		$program_name=ucfirst(str_replace("-"," ",$split_string[0]));
		echo "\">".$program_name."</a></td><td>".$language."</td></tr>";
	}
}
?>

</table>
<br>
<br>
<br>
</div>
</body>
</html>
