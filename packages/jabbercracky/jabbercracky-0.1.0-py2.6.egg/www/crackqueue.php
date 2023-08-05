<?php
    $db_connection = new mysqli("localhost", "crackuser", "crackpw", "crackqueue");
    $err_msg = "";
    
    if( isset( $_POST["hash"] ) && !empty( $_POST["hash"] ) 
   && isset( $_POST["type"] ) && !empty( $_POST["hash"] ) ) {
   
    // validate parameters
    $type = trim($_POST["type"]);
    $hash = trim($_POST["hash"]);
   
    if( $type != "md5" && $type != "lm" && $type != "halflm" && $type != "ntlm") {
        $err_msg = "INVALID HASH TYPE";
    }
    else if( strlen(trim( $hash, "1234567890abcdefABCDEF" )) ) {
        $err_msg = "HASH MUST BE IN HEXADECIMAL FORMAT";
    }
    else if($type == "md5" && strlen($hash) != 32){
        $err_msg = "MD5 MUST BE 32 HEX DIGITS";
    }
    else if($type == "lm" && strlen($hash) != 16){
        $err_msg = "LM MUST BE 16 HEX DIGITS";
    }
    else {
       // before submitting, make sure this isn't a duplicate
       $chk = $db_connection->prepare("SELECT * FROM queue WHERE type=? AND hash=?;");
       $chk->bind_param("ss", $type, $hash);
       $chk->execute();
       $row_count = 0;
       while ($chk->fetch()) {
        $row_count++;
       }
       $chk->close();
       
       if( $row_count != 0 ) {
        $err_msg = "HASH HAS ALREADY BEEN SUBMITTED";
       }
       else {
        // Also some metering by IP address. Won't work vs. proxies.
        $bfd = $db_connection->prepare("SELECT * FROM queue WHERE created > DATE_SUB(NOW(), INTERVAL 1 HOUR) AND src_ip=?;");
        $bfd->bind_param("s", $_SERVER['REMOTE_ADDR']);
        $bfd->execute();
        $rcnt = 0;
        while ($bfd->fetch()) {
          $rcnt++;
        }
        $bfd->close();
          
        if($rcnt > 4) {
           $err_msg = "HOURLY LIMIT EXCEEDED, TRY AGAIN LATER";
        }
        else {
	       $ins = $db_connection->prepare("INSERT INTO queue (type,src_ip,hash,created) VALUES(?, ?, ?, now());");
	       $ins->bind_param("sss", $type, $_SERVER['REMOTE_ADDR'], strtolower($hash));
	       $ins->execute();
	       $ins->close();       	       
        }
       }
       
    }
  }
?>
<html>
<head>
<title>hash.colab.hack</title>
</head>
<body>
<?php echo $err_msg; ?>
<form action="crackqueue.php" method="post">
	<input type="text" size="32" name="hash" />
	<select name="type">
		<option value="md5" selected="selected">MD5</option>
		<option value="lm">LM</option>
		<option value="ntlm">NTLM</option>
		<option value="halflm">Half LM/Challenge</option>
	</select>
	<input type="submit" value="Submit" />
</form>

<table border="1">
<tr>
<th>Type</th>
<th>Hash</th>
<th>Submitted</th>
<th>Clear</th>
<th>Started</th>
<th>Cracked</th>
</tr>

<?php	
	$query = "SELECT type, hash, created, clear, started, cracked FROM queue ORDER BY created DESC";
	if ($stmt = $db_connection->prepare($query)) {
		$stmt->execute();
		$stmt->bind_result($type, $hash, $created, $clear, $started, $cracked);

		while ($stmt->fetch()) {
                        $hashesc = htmlspecialchars($hash);
                        $clearesc = htmlspecialchars($clear);
			printf ("<tr>\n");
			printf ("<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>\n", 
			 $type, $hashesc, $created, $clearesc, $started, $cracked);
			printf ("</tr>\n");
		}
		$stmt->close();
	}
?>
</table> 

<?php include("news.inc"); ?>

</body>
</html>

<?php
/* close connection */
$db_connection->close();
?>
