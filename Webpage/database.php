<?php
// Establishing the connection with the database 
// Host: 127.0.0.1, username:root, password: flexilab, database: flexilab
$con = mysqli_connect("127.0.0.1","root","purdue","flexilab");

if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
?>