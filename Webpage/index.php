<!DOCTYPE html>
<!DOCTYPE html>
<html lang="en">
<head>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php
    // Importing the head code and the libraries 
    include("head.php");
    // Setting PIN 18 and 11 as an output mode 
	exec("fast-gpio set-output 18");
	exec("fast-gpio set-output 11");
	// Setting PIN 11 in zero for default 
	exec("fast-gpio set 11 0");

    ?>
    
<style>

/*
CSS to define the jumbotron. It permits to create a space with some characteristics in order to add an image or only for layout improvement. 
*/
	.jumbotron{
		background-color:#010101;
		color:white;
		padding-top: 0.5px;
    	padding-bottom:0.15px;
    	/*
    	Setting the initial configuration such as color and location 
    	*/
	}
	.jumbotron2{
		background-color:#;
		color:black;
		padding-top: 0.8px;
    	padding-bottom:0.10px;
    	/*
    	Setting the initial configuration such as color and location 
    	*/
	}
	
	.ct-line.ct-threshold-above, .ct-chart.ct-threshold-above, .ct-bar.ct-threshold-above, .ct-point.ct-threshold-above {
		stroke:	#0000A0;
			/*
    	Setting the initial configuration such as color and location 
    		#8B0000
    	*/
	
	}
	.ct-line.ct-threshold-below, .ct-chart.ct-threshold-below, .ct-bar.ct-threshold-below, .ct-point.ct-threshold-below {
		stroke: #000000;
	}
	body {background-color: #CACACA;}
	
</style>

</head>
<body>

<!-- Setting the initial layout of the Web-app application -->
<div class="page-header">
	<div class="jumbotron">
		<div class="text-center" >
			<h3>Universidad de Antioquia</h3>
		</div>

	</div>
</div>
<!-- The commands shown above define the head of the page. -->


<!-- Setting the initial layout in two columns -->
<div class="row p-1" style="margin: auto">

    <div class="col-sm-6" style="text-align: center;">
    	<div class="text-center">
			<h3>Campo de gráficas </h3>
		</div>
		<a href="http://192.168.3.1/adminer/">Presiona aquí para ver base de datos</a>
        <div class="col-sm-6"><div class="ct-chart" id="chart"></div></div>
        
        <div id="2000"></div>
        
		<!-- Creating buttons  -->
		<button type="button" style="background-color:rgb(255,255,255); border-color:white; color=white" class="btn btn-outline-light btn-lg" onclick="Setgraph(1)">Inciar</button>
        <button style="background-color:gray; border-color:white; color=white" class="btn btn-info btn-lg" onclick="Setgraph(0)">Parar</button>
		
		
		
		<!-- Each button calls a specific function according to the button's purpose -->
    </div>

    <div class="col-sm-6" style="text-align: center;">
	<!-- Defining a container which stores the tools and elements of the left layout of the Website-->
		<div class='Container'>
		<div class="jumbotron2">
			<div class="text-center" >
				<h3>Button Manager</h3>
			</div>
		</div>
		<figure>
			<img src="images/LED.jpg" width="280" height"155">
		</figure>
	<!-- Creating buttons  -->
		<button style="background-color:gray; border-color:white; color=white" class="btn btn-primary btn-lg" onclick="Setled(1)">ON</button>
        <button style="background-color:gray; border-color:white; color=white" class="btn btn-primary btn-lg" onclick="Setled(0)">OFF</button>
		</div>
    </div>
</div>
 
<script src="crud/graphic.js"> </script>

</body>
<!-- Functions in order to execute the commands -->

</html>