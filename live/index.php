<HTML> 
<head>
<Title>Subtitle Files</title>
<link rel="stylesheet" type="text/css" href="white.css">
</head>
<Body> 
<div id="columns">

<h1>Overview</h1>
This is the list of currently active files in the IMPS software:<br>
<?php 
$files1 = scandir(".");
//print_r($files1);
foreach ($files1 as $file){
	if (strpos($file,'html') !== false){
		echo "<a href=\"".$file;
		echo "\">".$file."</a><br>";
	}
}
?>

<br>
<br>
<br>
</div>
</body>
</html>
