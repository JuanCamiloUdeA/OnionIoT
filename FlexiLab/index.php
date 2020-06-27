<!DOCTYPE html>
<html lang="en">
<head>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">-->

    <?php

    include("head.php");

    //$led = $_GET["LED"];

	//exec("fast-gpio set-output 18");

	//if ($led == 0) {
        //exec("fast-gpio set 18 0");
    //}  // Setting the command how to power off a LED

	//if ($led == 1) {
        //exec("fast-gpio set 18 1");
    //}  // Setting the command how to power on a LED
    ?>
    
<style>
	.jumbotron{
		background-color:#010101;
		color:white;
		padding-top: 0.5px;
    	padding-bottom:0.10px;
	}
</style>


</head>
<body>

<!-- Setting the initial layout of the Web-app application -->
<div class="page-header">
	<div class="jumbotron">
		<div class="text-center" >
			<h3>Data Monitor and Button Manager Application - FlexiLab Purdue University</h3>
		</div>
		<div class="text-center">
			<img src="images/background.png" width="200" height="80">
		</div>
			
	</div>
</div>


<div class="row p-1" style="margin: auto">

    <div class="col-sm-6" style="text-align: center;">

        <!--<div class="ct-chart ct-perfect-fourth"></div>-->
        <div class="col-sm-6"><div class="ct-chart" id="chart"></div></div>

        <div id="2000"></div>

        <button class="btn btn-success btn-lg" onclick="viewerSignal(1)">Begin</button>
        <button class="btn btn-primary btn-lg" onclick="viewerSignal(0)">Stop</button>

    </div>

    <div class="col-sm-6" style="text-align: center;">
		
		<div class='Container'>
			
		<div class="jumbotron">
			<div class="text-center" >
				<h4>Plotting the Sensor Measures</h4>
			</div>
			<div class="text-center">
				<img src="images/ecg.jpg" width="50" height="50">
			</div>
		</div>
		
		<div class="jumbotron">
			<div class="text-center" >
				<h4>Button Manager, Voltage Output, and LED's Control</h4>
			</div>
			<div class="text-center">
				<img src="images/led.jpg" width="50" height="50">
			</div>
		</div>

        <!--<button class="btn btn-success btn-lg"onclick="location.href='index.php?LED=1'">High-Level</button>
        <button class="btn btn-primary btn-lg" onclick="location.href='index.php?LED=0'">Low-Level</button> -->
        
        <button class="btn btn-success btn-lg" onclick="Setled(1)">High-Level</button>
        <button class="btn btn-primary btn-lg" onclick="Setled(0)">Low-Level</button>
		
		</div>
    </div>
</div>
 



</body>


<script>
// Funcion Ajax del LED 
		function Setled(a){
		if (a===1){
			a=2;
			$.ajax({
				url: "crud/readLEDhigh.php"
			})
		}
		else if(a===0) {
			a=2;
			$.ajax({
				url: "crud/readLEDlow.php"
				})
			}
		}
    var signalData = [];
    var viewer = 0;

    function viewerSignal(key){viewer = key;}

    setInterval('signal()',250);

    $(document).ready(function(){

        var data = {

            labels: [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5],
        };

        var options = {
            width: '600px',
            height: '400px',
            showPoint: true,
            high: 3.3,
            low: 0,
            divisor: 0.1
        };

        new Chartist.Line('.ct-chart', data, options);}
    );

    function signal(){
    	
        if (viewer > 0){
        	
        	$.ajax({
        	url: "crud/readpython.php",
        	type: "post",
 
        	success: function (data) {
        		
        		//const num = JSON.parse(data);
        	
        		console.log(data);
        		//console.log(num.voltage);
      
            if(signalData.length > 9){signalData.shift();}

            //signalData.push(getRandomInt(0, 50));
            signalData.push(data);
            //console.log(signalData);

            var options = {
                width: '600px',
            	height: '400px',
            	showPoint: true,
            	high: 3.3,
            	low: 0,
            	divisor: 0.1,
                plugins: [
                	Chartist.plugins.ctAxisTitle({
                		axisX:{
                			axisTitle: 'Time (seconds)',
                			axisClass: 'ct-axis-title',
                			offset:{
                				x:0,
                				y:30
                			},
                			textAnchor: 'middle'
                		},
                		axisY:{
                			axisTitle: 'Volts (V)',
                			axisClass: 'ct-axis-title',
                			offset:{
                				x:-1,
                				y:0
                			},
                			textAnchor: 'middle',
                			flipTitle: false
                		}
                	})
                	]
                
                
                
            };

            var data = {
                // A labels array that can contain any sort of values
                //labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                labels: [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5],
                // Our series array that contains series objects or in this case series data arrays
                /*series: [
                    [1, 2, 4, 9, 0]
                ]*/

                series: [signalData],};

            new Chartist.Line('.ct-chart', data, options);

            //document.getElementById('1956').innerHTML=signal;
        }});
    	
        	
        }
    	
    }

    function getRandomArbitrary(min, max){
        return Math.random() * (max - min) + min;
    }

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

</script>

</html>