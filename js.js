
var url = 'canada.php';
var regionStats;
var canadaStats;

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
    
    
        var div = document.getElementById("dom-target");
        for (line in div){
          console.log(line);
        }

        getStats(url)
    .then((data) => {
      displayCases();
    });

    

}

function displayCases(){
    for (i = 0; i < regionStats.length; i++){
        
  
    var row = regionStats[i];
    var province = row.ProvinceName;
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
          radius: Math.sqrt(row.NumberOfCases) * 250,
          name: regionName,
          numberOfCases: numberOfCases,
          province:province
      });

      google.maps.event.addListener(cityCircle, 'click', function(ev) {
        map.panTo(this.center);       
        html = "<div id= 'region'>"+ this.province+ " , "+this.name+"</div>"+"<div id= 'cases'>Positive Cases: "+ this.numberOfCases+"</div>";

        document.getElementById("regionName").innerHTML = html;

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


  
