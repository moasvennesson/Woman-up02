//prints the variabel position
var x = document.getElementById("your-location"), latitude,  longitude, accruacy;
var Colors = ["Red","Orange","Yellow","Cyan","Blue","Purple","Pink","White","Gray","Brown"];
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

var mymap
function showPosition(position) {
  //saves your location i var latitude, longitude and accuracy
  latitude = position.coords.latitude;
  longitude = position.coords.longitude;
  accruacy = position.coords.accuracy; 
  getMap();
}

function getMap(){
    //map object
    mymap = L.map('mapid').setView([latitude, longitude], 13);
    //Generates a map layer
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);
   L.marker([latitude,longitude]).addTo(mymap).bindPopup("<b>Din plats </b>").openPopup();
    //L.marker gives a pin the position (your position)
    var circle = L.circle([latitude, longitude], {
        color: 'green',
        fillColor: 'green',
        fillOpacity: 0.5,
        radius: accruacy
    }).addTo(mymap);
   
 
 
    addEmergencyMessageOnMap(mymap);
}
 
//adds the emergency message to the map
function addEmergencyMap(NamnF,pos,text,date,mymap){
  for (i = 0; i < NamnF.length-1; i++) {
      a = i*3;
      if(NamnF[i] != null &&  pos!= null){
        L.marker([pos[a],pos[(a+1)]]).addTo(mymap).bindPopup("<b>"+NamnF[i]+"</b> " +text + "datum " + date);
        var circle = L.circle([poslat[i], poslon[i]], {
            color: 'Blue',
            fillColor: 'Purple',
            fillOpacity: 0.5,
            radius: Offset[a+3]
        }).addTo(mymap);
    }
  }
 

}
 

//Collects the message from emergency and adds it to a pin
function addEmergencyMessageOnMap(mymap){
    var stringtoarray;
    var NamnF = [];
    var poslat= [];
    var poslon= [];
    var Offset= [];
    stringtoarray = document.getElementById("SendName").innerHTML;
    NamnF = stringtoarray.split(";");
    stringtoarray = document.getElementById("Pos").innerHTML;
    pos = stringtoarray.split(",");
    stringtoarray = document.getElementById("text").innerHTML;
    text = stringtoarray.split(";");
    stringtoarray = document.getElementById("date").innerHTML;
    date = stringtoarray.split(";");
    addEmergencyMap(NamnF,pos,text,date,mymap);
 
}

getLocation();