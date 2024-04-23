const pops = document.getElementById("pops")
pops.addEventListener('click', function(event) {
    if (event.target === pops) {
        pops.style.display = "none" ;
    }
});


function sendmsgEnter(event) {
  if (event.key === "Enter") {
    sendmsg();
  }
}
