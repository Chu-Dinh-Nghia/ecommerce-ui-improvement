"use strict";

const $ = id => document.getElementById(id);
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

let level, xp, strength, agility, intel, health;
let dragonHealth, dragonStr, maxHealth;
let busy = false, auto = false, gameContinue = true;

function log(message) {
  const li = document.createElement("li");
  li.textContent = message;
  $("log").prepend(li);

  if ($("log").children.length > 60) {
    $("log").lastChild.remove();
  }
}

function update() {
  $("heroHP").textContent = `${health} / ${maxHealth} HP`;
  $("dragonHP").textContent = `${dragonHealth} / 600 HP`;

  $("heroBar").style.width = health / maxHealth * 100 + "%";
  $("dragonBar").style.width = dragonHealth / 600 * 100 + "%";

  $("stats").textContent =
    `Cấp ${level} | XP ${xp} | STR ${strength}` +
    ` | AGI ${agility} | INT ${intel}`;

  $("attack").disabled = busy || auto || !gameContinue;
  $("reset").disabled = busy;
  $("auto").disabled = !gameContinue;
  $("auto").textContent = auto ? "Ⅱ Dừng tự động" : "▶ Tự động";

  for (const id of ["name", "role", "mode"]) {
    $(id).disabled = busy || auto;
  }
}

function resetGame() {
  auto = false;
  gameContinue = true;

  // Giữ công thức tính chỉ số trong code của bạn.
  level = 2;
  xp = 150 * (level - 1) + 200;
  const skillpoints = 5 + xp / 10;

  strength = 0.6 * skillpoints + 0.1 * xp;
  agility = 0.2 * skillpoints + 0.2 * xp;
  intel = 0.2 * skillpoints + 10 * level;

  level = 3;
  xp += 200;

  const heroName = $("name").value.trim() || "Chu Đình Nghĩa";
  $("heroName").textContent = heroName;

  // Giữ thưởng/phạt INT khi nhập tên như bài gốc.
  intel += heroName === "Chu Đình Nghĩa" ? 5 : -5;

  switch ($("role").value) {
    case "a":
      strength += 15;
      agility -= 10;
      intel -= 5;
      break;
    case "b":
      strength -= 15;
      agility += 10;
      intel += 5;
      break;
    case "c":
      strength -= 15;
      intel += 15;
      break;
  }

  level = 4;
  xp += 700;
  level = 5;

  // Luyện tập giúp trận đấu kéo dài hơn.
  const practice = $("mode").value === "practice";
  maxHealth = practice ? 420 : level + 100;
  dragonStr = practice ? 28 : 100;

  health = maxHealth;
  dragonHealth = 600;

  $("hero").className = "fighter";
  $("dragon").className = "fighter";
  $("result").textContent = "";
  $("log").replaceChildren();

  log("Trận đấu bắt đầu! Hãy nhấn Tấn công hoặc Tự động.");
  update();
}

// Lấy tâm nhân vật, tính theo vị trí trong đấu trường.
function position(id) {
  const arena = $("arena").getBoundingClientRect();
  const box = $(id).getBoundingClientRect();

  return {
    x: box.left - arena.left + box.width / 2,
    y: box.top - arena.top + box.height / 2
  };
}

async function attackEffect(attacker, target, hit, damage, critical) {
  $(attacker).classList.add("attack");
  await wait(200);

  const from = position(attacker);
  const to = position(target);

  const shot = document.createElement("div");
  shot.className = "shot";
  shot.style.color = attacker === "hero" ? "#65dbff" : "#ff7028";
  $("arena").append(shot);

  // Đạn phép hoặc hỏa cầu bay đến đối thủ.
  const animation = shot.animate([
    { left: from.x + "px", top: from.y + "px" },
    { left: to.x + "px", top: to.y + "px" }
  ], {
    duration: 450,
    easing: "ease-in",
    fill: "forwards"
  });

  await animation.finished;
  shot.remove();
  $(attacker).classList.remove("attack");

  $(target).classList.add(hit ? "hurt" : "dodge");

  const text = document.createElement("div");
  text.className = "damage";
  text.style.left = Math.max(10, to.x - 55) + "px";
  text.style.top = to.y + "px";
  text.textContent = hit
    ? `${critical ? "CHÍ MẠNG " : ""}−${damage}`
    : "NÉ ĐÒN!";

  $("arena").append(text);
  setTimeout(() => text.remove(), 1000);

  // Chỉ trừ máu khi đạn đến nơi và đánh trúng.
  if (hit) {
    if (target === "dragon") {
      dragonHealth = Math.max(0, dragonHealth - damage);
    } else {
      health = Math.max(0, health - damage);
    }
  }

  update();
  await wait(550);
  $(target).classList.remove("hurt", "dodge");
}

function finish(won) {
  gameContinue = false;
  auto = false;

  if (won) {
    level = 6;
    xp += 600;
    $("dragon").classList.add("dead");
    $("result").textContent = "🏆 CHIẾN THẮNG! Cấp 6 — XP +600";
    log("Bạn đạt danh hiệu Dũng sĩ diệt Rồng!");
  } else {
    $("hero").classList.add("dead");
    $("result").textContent = "💀 THẤT BẠI! Nhấn Chơi lại.";
    log("Anh hùng đã gục ngã.");
  }
}

async function playTurn() {
  if (busy || !gameContinue) return;

  busy = true;
  update();

  try {
    // Anh hùng tấn công: rồng có AGI = 15.
    const heroHit = Math.random() * 100 > 15;
    const heroCritical = heroHit && Math.random() * 100 < intel;

    // Theo code gốc: đòn thường + thêm 2 × STR = tổng 3 × STR.
    const heroDamage = strength * (heroCritical ? 3 : 1);

    await attackEffect(
      "hero", "dragon", heroHit, heroDamage, heroCritical
    );

    log(heroHit
      ? `TRẢM LONG! ${heroCritical ? "Chí mạng! " : ""}Rồng mất ${heroDamage} HP.`
      : "Rồng đã né được đòn đánh!");

    if (dragonHealth <= 0) {
      finish(true);
      return;
    }

    await wait(250);

    // Rồng phản công: giữ INT = 80 như code gốc.
    const dragonHit = Math.random() * 100 > agility;
    const dragonCritical = dragonHit && Math.random() * 100 < 80;
    const dragonDamage = dragonStr * (dragonCritical ? 3 : 1);

    await attackEffect(
      "dragon", "hero", dragonHit, dragonDamage, dragonCritical
    );

    log(dragonHit
      ? `HỎA CẦU! ${dragonCritical ? "Chí mạng! " : ""}Bạn mất ${dragonDamage} HP.`
      : "Bạn đã né được hỏa cầu!");

    if (health <= 0) finish(false);
  } catch (error) {
    auto = false;
    log("Không chạy được hoạt ảnh. Hãy mở bằng Chrome hoặc Edge mới.");
    console.error(error);
  } finally {
    busy = false;
    update();

    if (auto && gameContinue) {
      setTimeout(() => {
        if (auto) playTurn();
      }, 500);
    }
  }
}

$("attack").addEventListener("click", playTurn);
$("reset").addEventListener("click", resetGame);

$("auto").addEventListener("click", () => {
  auto = !auto;
  update();
  if (auto && !busy) playTurn();
});

for (const id of ["name", "role", "mode"]) {
  $(id).addEventListener("change", resetGame);
}

resetGame();