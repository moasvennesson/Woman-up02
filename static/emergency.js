

function text1(){
    var rop ="Hejsan! Ska hem nu, hade du kunnat följa mig?";
    document.getElementById("Truta").innerHTML = rop;
}

function text2(){
    var rop ="Jag är i fara hjälp mig!";
    document.getElementById("Truta").innerHTML = rop;
}

function text3(){
    var rop ="Någon förföljer mig. Kan du hjälpa mig?";
    document.getElementById("Truta").innerHTML = rop;
}

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      x.innerHTML = "Geolocation is not supported by this browser.";
    }
  }
  
function showPosition(position) {
    //sparar din plats i var latitude, longityde och accruacy
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    accruacy = position.coords.accuracy; 
    document.getElementById("pos").value = (latitude + "," + longitude + "," + accruacy);
  
  }
getLocation();
