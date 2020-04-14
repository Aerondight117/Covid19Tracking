<!DOCTYPE html>

<html>
  <head>
  
    <link rel="stylesheet" type="text/css" href="style.css">

    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Covid Spread In Canada</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 90%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>

  <body>
    
    <div id="map"></div>
    <script>

    var url = 'canada.php';
    var map;



    var canadaStats = getStats(url);
  
    function getStats(url){
      fetch(url)
        .then(res => res.json())
        .then((out) => {
          canadaStats = out;
            drawCircles(map);
          })
      .catch(err => { throw err });
    };

    function drawCircles(map){
      for (line in canadaStats){
        //set the variables 
        var numberOfCases = canadaStats[line].NumberOfCases;
        var latitude = canadaStats[line].Latitude;
        var longitude = canadaStats[line].Longitude;

        var latLong =  {lat: parseFloat(latitude), lng: parseFloat(longitude)};


        var cityCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: latLong,
            radius: Math.sqrt(numberOfCases) * 100
        });
    
      }

    };

    


    function initMap() {

      // Create the map.
      map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {lat: 53.7609, lng: -98.8139},
        mapTypeId: 'roadmap'
      });

        
        

        

      };
      

    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCYK-dXBFgT2pX4-b8z0q3LLmLGCP75GNc&callback=initMap">
    </script>

    <div id = "title">Covid Spread In Canada</div>

    <div id = "information">

    The aim of this website is to display Canada's data of covid-19 cases.
    </br>
    This data is collected from the official provincial data.
    
    </br>
    Ontario
    <?php
    echo '<ul>'
    for (line in canadaStats){
      echo line;
    }

    ?>
    </br>
    https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/4f39b02b-47fe-4e66-95b6-e6da879c6910
    
    </br>

    Quebec
    </br>
    https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/
    </br>
    
    BC
    </br>
    http://www.bccdc.ca/health-info/diseases-conditions/covid-19/case-counts-press-statements
    </br>

      
    <div>
  </body>
</html>