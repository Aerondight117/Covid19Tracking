
var url = 'canada.php';
var regionStats;
var canadaStats;
var cityCircles;
var map;


function formatNumber(num) {
  return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

async function getStats(url){
    const response = await fetch(url)
    .then(response => response.json())
    .then((data) => {
        setstats(data);
        //showTotal();
        fillStats();
      })
  .catch(err => { throw err });
  return response;
}

getStats(url)
    .then((data) => {
      displayCases();
    });

function setstats(data){
    regionStats = data.region;
    canadaStats = data.canada;
}



function initMap() {

    var latitude = 53.7609;
    var longitude = -90.8139;
    var latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};

    // Create the map.
        map = new google.maps.Map(  document.getElementById('map'), {
        center: latlng,
        zoom: 4,
        mapTypeId: 'roadmap',
        options: {gestureHandling: 'greedy'}
        });
    
    


}

function displayCases(){
    for (i = 0; i < regionStats.length; i++){
        
  
    var row = regionStats[i];
    
    var regionName = row.RegionName;
    var numberOfCases = row.NumberOfCases;
    var latitude = row.Latitude;
    var longitude = row.Longitude;
  
    if (numberOfCases>0){
      var latLong = {lat: parseFloat(row.Latitude), lng: parseFloat(row.Longitude)};
       cityCircle = new google.maps.Circle({
          strokeColor: '#FF0000',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#FF0000',
          fillOpacity: 0.35,
          map: map,
          center: latLong,
          radius: Math.sqrt(row.NumberOfCases) * 250
      });
    }
  }
  }



  function fillStats(){
    i = 0;
    
    while(i < canadaStats.length){
      row = canadaStats[i];
      html = "<div id= '" +row.RegionName + "' onclick='(map.setCenter({lat: " + parseFloat(row.Latitude) + ",  lng: " + parseFloat(row.Longitude) + "}, map.setZoom("+ row.zoomLevel+")) ) ' class='stat'><div class='regionName'> <h4>" + row.RegionName +  "</h4> </div>  <div id = 'regionStats'> Cases: " + formatNumber(row.NumberOfCases)+ "<br> Deaths: " + formatNumber(row.Deaths) + "<br> Tested: " + formatNumber(row.NumberTested) + "</div></div>";

      document.getElementById("stats").innerHTML += html;

      i++;
    };
    
  }


  
  function getOntario(){
      latitude = 50.2434053;
      longitude = -90.4794775;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(6);
    }
  
    function getCanada(){
      latitude = 53.7609;
      longitude = -90.8139;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(4);
    }

    function getQuebec(){
      latitude = 53.4737266;
      longitude = -77.3971109;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(5);
    }

    function getBC(){
      latitude = 53.7911033
      longitude = -135.5095492;
      latlng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
      map.setCenter(latlng);
      map.setZoom(5);
    }

