document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, options);
});

// Or with jQuery

$(document).ready(function(){
  $('.sidenav').sidenav();
});





// javascript till kartan

//skriver ut postion variablen
var x = document.getElementById("DinPlats"), latitude,  longitude, accruacy;
//används till att ge färger till vännerna.
var Colors = ["Red","Orange","Yellow","Cyan","Blue","Purple","Pink","White","Gray","Brown"];
document.getElementById("spara_plats").value = "test";
function success(position) {
    //sparar din plats i var latitude, longityde och accruacy
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    accruacy = position.coords.accuracy;
    document.getElementById("spara_plats").value = (latitude + "," + longitude + "," + accruacy);
    //skriver till var x
    x.innerHTML = latitude + " " + longitude + " accruacy: inom "+ accruacy + "m från din riktiga position";

    getMap();
    
  }
// kan inte hitta din plats
function error() {
    alert('Sorry, no position available.');
  }
// Ska bli bättre position
const options = {
    enableHighAccuracy: true, 
    maximumAge: 30000, 
    timeout: 27000
  };
//Uppdaterar position
const watchID = navigator.geolocation.watchPosition(success, error, options);


function getMap(){
    //kart objektet
    var mymap = L.map('mapid').setView([latitude, longitude], 15);
    //Genererar en karta layer
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
    //L.marker ger en pin på platsen (på din plats)
    var circle = L.circle([latitude, longitude], {
        color: 'green',
        fillColor: 'green',
        fillOpacity: 0.5,
        radius: accruacy
    }).addTo(mymap);
   
 
 
    getDatabaseFriendsOnMap(mymap);
}
 
//lägger till vänner på kartan
function getFriendsMap(FriendsName,poslat,poslon,Offset,mymap){
  for (i = 0; i < FriendsName.length-1; i++) {
      if(FriendsName[i] != null &&  poslat!= null && poslon != null){
      // använder Colors array för att ge färg till Personer L.marker ger en pin på platsen
        L.marker([poslat[i],poslon[i]]).addTo(mymap).bindPopup("<b>"+FriendsName[i]+"</b>");
        var circle = L.circle([poslat[i], poslon[i]], {
            color: 'Blue',
            fillColor: 'Purple',
            fillOpacity: 0.5,
            radius: Offset[i]
        }).addTo(mymap);
    }
  }
 

}
 
//skriv ut de som är på karta
 function printKarta(){
    var printContents = document.getElementById("mapid").innerHTML;
    var originalContents = document.body.innerHTML;
    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
 
}
//Hämtar alla värden och lägger en pin på de
function getDatabaseFriendsOnMap(mymap){
    var stringtoarray;
    var NamnF = [];
    var poslat= [];
    var poslon= [];
    var Offset= [];
    //Hämtar input från databasen
    //Formatet måste , mellan varje
    stringtoarray = document.getElementById("SendName").innerHTML;
    NamnF = stringtoarray.split(",");
    stringtoarray = document.getElementById("SendLat").innerHTML;
    poslat = stringtoarray.split(",");
    stringtoarray = document.getElementById("SendLong").innerHTML;
    poslon = stringtoarray.split(",");
    stringtoarray = document.getElementById("SendOffset").innerHTML;
    Offset = stringtoarray.split(",");
    ////////////////////////////////////////////////////////////////
    // 3 arrayer latitud longitud Namn
    getFriendsMap(NamnF,poslat,poslon,Offset,mymap);
 
}
 

//De vi startar direkt
//skriver datumet
//document.write(Date());



