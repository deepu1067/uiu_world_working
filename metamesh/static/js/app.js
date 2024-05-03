const pops = document.getElementById("pops");
pops.addEventListener("click", function (event) {
  if (event.target === pops) {
    pops.style.display = "none";
  }
});

function sendmsgEnter(event) {
  if (event.key === "Enter") {
    sendmsg();
  }
}

function scrollToBottom() {
  setTimeout(() => {
      var msgContainer = document.getElementById('showmsg');
      msgContainer.scroll({
          top: msgContainer.scrollHeight,
          behavior: 'smooth'
      });
      console.log("Scrolled to bottom");
  }, 300); 
}