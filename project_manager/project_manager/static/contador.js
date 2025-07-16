const countdownBox = document.getElementById('countdown-box');

function updateCountdown() {
  const now = Date.now() / 1000; // epoch en segundos
  let secondsLeft = Math.floor(deleteTime - now);

  if (secondsLeft <= 0) {
    countdownBox.innerText = "Borrando en: 00:00";
    setTimeout(() => location.reload(), 1000);  // refresca la página después de 1 segundo
    return;
  }

  const minutes = String(Math.floor(secondsLeft / 60)).padStart(2, '0');
  const seconds = String(secondsLeft % 60).padStart(2, '0');

  countdownBox.innerText = `Borrando en: ${minutes}:${seconds}`;
}

updateCountdown();
setInterval(updateCountdown, 1000);