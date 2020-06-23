var countDownDate = new Date("Jun 20, 2020 15:37:25").getTime();

var min = JSON.parse({{pprDet|tojson}});
console.log(min);
min = min * 60 * 1000;

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = min;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  if(days == 0){
    document.getElementById("timer").innerHTML = "&#128337" + hours + "h "
    + minutes + "m " + seconds + "s ";
  }
  else {
    document.getElementById("timer").innerHTML = "&#128337" + days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
  }
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "&#128337" + "EXPIRED";
  }
}, 1000);