<?php
// Include config file
require_once "config.php";
        
if ($result =  $mysqli-> query("SELECT * FROM covicivy_covidCasesInCanada.CovidCasesQuebec")) {
 
  while($row = $result->fetch_array(MYSQLI_ASSOC)) {
    $myArray[] = $row;
  }
  
  echo json_encode($myArray);
  
  $result -> free_result();
    }
 ?>
