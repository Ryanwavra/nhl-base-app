export function getDailyGames() {
  return [
    { id: 1, home: "Toronto Maple Leafs", away: "Montreal Canadiens", time: "7:00 PM" },
    { id: 2, home: "Boston Bruins", away: "Florida Panthers", time: "7:30 PM" }
  ];
}

export function renderGames(games) {
  let html = "";
  for (let game of games) {
    html += `
      <div class="game">
        <h3>${game.away} @ ${game.home} (${game.time})</h3>
        <label><input type="radio" name="game-${game.id}" value="away"> ${game.away}</label>
        <label><input type="radio" name="game-${game.id}" value="home"> ${game.home}</label>
      </div>
    `;
  }
  return html;
}

export function getFirstPuckDrop() {
  const games = getDailyGames();
  const firstGameTime = games[0].time; // Earliest: 7:00 PM
  const [time, period] = firstGameTime.split(" ");
  let [hours, minutes] = time.split(":").map(Number);
  if (period === "PM" && hours !== 12) hours += 12;
  const today = new Date();
  return new Date(today.getFullYear(), today.getMonth(), today.getDate(), hours, minutes - 5); // 5 min before
}