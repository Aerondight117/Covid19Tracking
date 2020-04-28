<?php
// Include config file
require_once "config.php";


if ($result =  $mysqli-> query("SELECT * FROM covicivy_covidCasesInCanada.CovidCasesInCanadaWithMissingData")) {

  while($row = $result->fetch_array(MYSQLI_ASSOC)) {
    $myArray[] = $row;
  }

  $result -> free_result();
}

if ($result =  $mysqli-> query("SELECT * FROM covicivy_covidCasesInCanada.CovidCasesCanada ORDER BY NumberOfCases DESC")) {

    while($row = $result->fetch_array(MYSQLI_ASSOC)) {
      $myArray2[] = $row;
    }
  
    $result -> free_result();
  }
  


  



echo json_encode(array('region' => $myArray,'canada' =>  $myArray2));
    
 ?>
