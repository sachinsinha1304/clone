var t = {{time}};
const time = document.getElementById('timer');

setInterval(updateTimer, 1000);

function updateTimer() {
    t--;
   time.innerHTML = t;
}