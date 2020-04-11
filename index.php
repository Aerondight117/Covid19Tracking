<!DOCTYPE html>

<html>
  <head>
  
    <link rel="stylesheet" type="text/css" href="mystyle.css">

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
    <div id = "title">Covid Spread In Canada</div>
    <div id="map"></div>
    <script>

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        ontarioStats = JSON.parse(this.responseText);
        
      }
    };
    xmlhttp.open("GET", "ontario.php", true);
    xmlhttp.send();

    
    xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        quebecStats = JSON.parse(this.responseText);
        
      }
    };
    xmlhttp.open("GET", "quebec.php", true);
    xmlhttp.send();





      function initMap() {
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: {lat: 53.7609, lng: -98.8139},
          mapTypeId: 'roadmap'
        });

    

        for (line in quebecStats) {
        
          
          //set the variables 
          var numberOfCases = quebecStats[line].number_of_cases;
          var latitude = quebecStats[line].region_lat;
          var longitude = quebecStats[line].region_long;

          var latLong =  {lat: parseFloat(latitude), lng: parseFloat(longitude)};


          var cityCircle = new google.maps.Circle({
              strokeColor: '#0008ff',
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: '#0008ff',
              fillOpacity: 0.35,
              map: map,
              center: latLong,
              radius: Math.sqrt(numberOfCases) * 100
            });
        }

        for (line in ontarioStats) {
        
        //set the variables 
        var numberOfCases = ontarioStats[line].NumberOfCases;
        var latitude = ontarioStats[line].Reporting_PHU_Latitude;
        var longitude = ontarioStats[line].Reporting_PHU_Longitude;

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

    

              // Try HTML5 geolocation.
              if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCYK-dXBFgT2pX4-b8z0q3LLmLGCP75GNc&callback=initMap">
    </script>

    <div id = "information">

    The aim of this website is to display Canada's data of covid-19 cases.
    </br>
    This data is collected from the official provincial data.
    
    </br>
    Ontario
    

    </br>
    https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/4f39b02b-47fe-4e66-95b6-e6da879c6910
    
    </br>

    Quebec
    </br>
    https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/
    </br>


      
    <div>
  </body>
</html>