
<?php
// Command to exec the Onion Pin in High in order to begin the Python code
// Set the high value in order to begin to store the information
exec("fast-gpio set 18 1");
exec("python /root/python_codes//FlexiLab/adc_new_code.py");
?>