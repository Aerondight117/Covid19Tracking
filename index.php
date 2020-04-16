<!DOCTYPE html>

<html>

<script>

var url = 'canada.php';
var map;



var regionStats = getStats(url);
var canadaStats;


function drawCircles(map){
  for (line in regionStats){
    //set the variables 
    var numberOfCases = regionStats[line].NumberOfCases;
    var latitude = regionStats[line].Latitude;
    var longitude = regionStats[line].Longitude;

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


function getStats(url){
  fetch(url)
    .then(res => res.json())
    .then((out) => {
      regionStats = out.region;
      canadaStats = out.canada;
        drawCircles(map);
        //showTotal();
        getCanada();
        fillStats();
        
          
      })
  .catch(err => { throw err });
};

function initMap() {

  // Create the map.
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 53.7609, lng: -98.8139},
    mapTypeId: 'roadmap',
    options: {
      gestureHandling: 'greedy'
    }
  });

    
    

    

  };
  

</script>


  <head>
  
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Map Of Covid - 19 Tests</title>

  </head>

  <body>
    
    <div id="map"></div>

    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCYK-dXBFgT2pX4-b8z0q3LLmLGCP75GNc&callback=initMap">
    </script>
<div id="navigation">
    <div id = "title"><h2>Map of provincial and federal Covid-19 data.<h2></div>
      <div id = "canada">
        <div id = "information">
          <div id="stats">
          </div>
        </div>
    </div>

</div>


  </body>


  <script>
  function fillStats(){
    i = 0;
    
    while(i < canadaStats.length){
      row = canadaStats[i];
      html = "<div id= '" +row.RegionName + "' class='stat'> <h4>" + row.RegionName +  "</h4> <br> Cases: " + row.NumberOfCases + "<br> Deaths: " + row.Deaths + "<br></div>";

      document.getElementById("stats").innerHTML += html;

      i++;
    };
    
  };
  
  function getOntario(){
      latitude = 50.2434053;
      longitude = -90.4794775;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(5);
    };
  
    function getCanada(){
      latitude = 53.7609;
      longitude = -90.8139;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(4);
    };

    function getQuebec(){
      latitude = 53.4737266;
      longitude = -77.3971109;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(5);
    };

    function getBC(){
      latitude = 53.7911033
      longitude = -135.5095492;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(5);
    };
    </script>

  </html>