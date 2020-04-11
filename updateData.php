
<?php

$db = new SQLite3('CanadaCovidResults.db');


$results = $db->query("SELECT * FROM CovidCasesCanada");

while ($row = $res->fetchArray()) {
    echo "{$row['NumberOfCases']} {$row['Reporting_PHU_Latitude']} {$row['Reporting_PHU_Longitude']} \n";
}

$db->close();

?>