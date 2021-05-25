<?php
// Include config file
require_once "config.php";

// The data will be stored in these 2 arrays
$RegionDataArray =[];
$ProvincialDataArray = [];

//Get the regional data from DB
if ($result =  $mysqli-> query("SELECT * FROM covicivy_covidCasesInCanada.CovidCasesInCanadaWithMissingData ")) {

  //populate the array row by row
  while($row = $result->fetch_array(MYSQLI_ASSOC)) {
    $RegionDataArray[] = $row;
  }

  //free the result now that its not used
  $result -> free_result();
}

// get the provincial data from the DB
if ($result =  $mysqli-> query("SELECT * FROM covicivy_covidCasesInCanada.CovidCasesCanada ORDER BY NumberOfCases DESC")) {

  //populate the array row by row  
  while($row = $result->fetch_array(MYSQLI_ASSOC)) {
    $ProvincialDataArray[] = $row;
  }

  //free the result now that its not used
  $result -> free_result();
}
  

// Helper function to convert the data in the arrays into UTF8
// This fixes anglicized names in Quebec
function utf8ize( $mixed ) {
  if (is_array($mixed)) {
      foreach ($mixed as $key => $value) {
          $mixed[$key] = utf8ize($value);
      }
  } elseif (is_string($mixed)) {
      return mb_convert_encoding($mixed, "UTF-8", "UTF-8");
  }
  return $mixed;
}


// create an array that holds the 2 data arrays that now have data in them
$data = array('region' => utf8ize($RegionDataArray),'canada' =>  utf8ize($ProvincialDataArray));
  
// Encode the Data Array as Json

$json = json_encode($data, JSON_UNESCAPED_UNICODE);

// check that the json is valid
if ($json === false) {
    // if the json is invalid echo the error string
    $json = json_encode(["jsonError" => json_last_error_msg()]);
    if ($json === false) {
        // This should not happen, but we go all the way now:
        $json = '{"jsonError":"unknown"}';
    }
    // Set HTTP response status code to: 500 - Internal Server Error
    http_response_code(500);
}
echo $json;
    