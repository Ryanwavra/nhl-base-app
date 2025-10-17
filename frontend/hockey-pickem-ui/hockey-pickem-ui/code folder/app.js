import { getDailyGames, renderGames, getFirstPuckDrop } from './games.js';

export let totalPlayers = 0;
export let totalPot = 0;

export function updatePotDisplay() {
  const playersDivs = document.querySelectorAll('#players-entered');
  const potDivs = document.querySelectorAll('#current-pot');
  playersDivs.forEach(div => {
    div.innerText = `${totalPlayers} Players Entered`;
  });
  potDivs.forEach(div => {
    div.innerText = `Current Pot: $${totalPot}`;
  });
}

export function startCountdown(callback) {
  const deadline = getFirstPuckDrop();
  const countdownDiv = document.getElementById('countdown');
  const submitBtn = document.getElementById('submit-btn');

  const timer = setInterval(function() {
    const now = new Date();
    const timeLeft = deadline - now;

    if (timeLeft <= 0) {
      clearInterval(timer);
      if (countdownDiv) countdownDiv.innerText = "Picks locked!";
      if (submitBtn) submitBtn.disabled = true;
      if (callback) callback();
      return;
    }

    const hoursLeft = Math.floor(timeLeft / (1000 * 60 * 60));
    const minutesLeft = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const secondsLeft = Math.floor((timeLeft % (1000 * 60)) / 1000);
    if (countdownDiv) {
      countdownDiv.innerText = `Picks lock in: ${hoursLeft}h ${minutesLeft}m ${secondsLeft}s`;
    }
  }, 1000);
}