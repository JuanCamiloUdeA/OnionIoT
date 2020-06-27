<?php

// Code to get the data from the database 

include("../database.php");
// Select the information from the table data the 10 last samples (For more information check the database on 192.168.3.1/adminer/) 
	$query = "SELECT * FROM data ORDER BY id DESC LIMIT 13"; 
// Getting the data 
    $result = mysqli_query($con, $query);
// Creating a variable like an array
    $signal = array();

while($row = mysqli_fetch_assoc($result)){
// Store the information in a variable called data from the row "voltage" available on the database
	$data['series'] = $row['voltage'];
	// Convert data as an array
	array_push($signal, $data);
}
// Convert the result in json format in order to plot through javascript 
echo json_encode($signal);

?>