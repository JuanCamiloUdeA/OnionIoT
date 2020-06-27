
	function Setled(a){
		if (a===1){
			a=2;
			$.ajax({
				url: "crud/readLEDhigh2.php"
			})
	 // Function to power on the LED. It is programmed with AJAX in order to avoid refreshing the website 
		}
		else if(a===0) {
			a=2;
			$.ajax({
				url: "crud/readLEDlow2.php"
				})
	 // Function to power off the LED. It is programmed with AJAX in order to avoid refreshing the website 

			}
		}
	function Setgraph(a){
		if (a===1){
			a=2;
			viewerSignal(1);
			$.ajax({
				url: "crud/readLEDhigh.php"
			})
			// Function to begin to store into the database. It also execute the code readLEGhigh.php
		
		}
		else if(a===0) {
			a=2;
			$.ajax({
				url: "crud/readLEDlow.php"
				})
			}
			 // Function to begin to stop storing into the database. It also execute the code readLEGlow.php
		}

    var signalData = [];
    var viewer = 0;
    
    // Function to plot according to Chartist.js 
    function viewerSignal(key){viewer = key;}
	// Plotting each 500 ms
    setInterval('signal()',500);

    $(document).ready(function(){

        var data = {

            labels: [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0],
        };
      // Setting the initial features of the plot grid 
        var options = {
            width: '700px',
            height: '400px',
            showPoint: true,
            high: 3.3,
            low: 0,
            divisor: 0.1,
           
            plugins: [
            	// Setting the names of the labels 
            		Chartist.plugins.ctThreshold({
    					threshold: 1
    				}),	
                	Chartist.plugins.ctAxisTitle({
                		axisX:{
                			axisTitle: 'Muestras',
                			axisClass: 'ct-axis-title',
                			offset:{
                				x:0,
                				y:30
                			},
                			textAnchor: 'middle'
                		},
                		axisY:{
                			axisTitle: 'Voltaje (V)',
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


        new Chartist.Line('.ct-chart', data, options);}
    // Plotting according to Chartist commands 
    );

    function signal(){
    	
    	var seriesajax = [];
    	
        if (viewer > 0){
        	// Reading the data from the database in order to plot in real-time 
        	$.ajax({
        	url: "crud/readmysql.php",
        	type: "post",
 
        	success: function (data) {
        		
        		const num = JSON.parse(data);
        	// Handling the JSON format 	
        		
        	
        	num.forEach(task => {
        		
        		seriesajax.push(task.series);
        	// Setting data as the plotting data 
        	})
        		
        		
            var options = {
                width: '700px',
            	height: '400px',
            	showArea:false,
            	showPoint: true,
            	high: 3.3,
            	low: 0,
            	divisor: 0.1,
                plugins: [
                	Chartist.plugins.ctThreshold({
    					threshold: 1
    				}),	
                	Chartist.plugins.ctAxisTitle({
                		axisX:{
                			axisTitle: 'Muestras ',
        	      			axisClass: 'ct-axis-title',
                			offset:{
                				x:0,
                				y:30
                			},
                			textAnchor: 'middle'
                		},
                		axisY:{
                			axisTitle: 'Voltaje (V)',
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
                labels: [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0],

                series: [seriesajax]};
                // Function to avoid refreshing the website 
            new Chartist.Line('.ct-chart', data, options);
            // Plotting the information according to the Chartist documentation 
        }});
    	
        	
        }
    	
    }
    	