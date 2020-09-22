function randInt(low, high) {
  const rndDec = Math.random();
  const rndInt = Math.floor(rndDec * (high - low + 1) + low);
  return rndInt;
}

function generateProblem(operation, maxNum) {
  let q, a;
  if (maxNum <= 0) maxNum = 20;
  if (operation === "addition") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(0, maxNum);
    q = String(num1) + " + " + String(num2);
    a = num1 + num2;
  } else if (operation === "subtraction") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(num1, maxNum);
    q = String(num2) + " - " + String(num1);
    a = num2 - num1;
  } else if (operation === "multiplication") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(0, maxNum);
    q = String(num1) + " x " + String(num2);
    a = num1 * num2;
  } else if (operation === "division") {
    const num1 = randInt(1, maxNum);
    const num2 = randInt(0, maxNum);
    const num3 = num1 * num2;
    q = String(num3) + " / " + String(num1);
    a = num2; 
  }
  return {"q" : q, "a" : a};
}

function saveScore(operation, maxNum, score) {
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
  const data = {
    'parameters': {
      'operation': operation,
      'max number': maxNum,
    },
    'score': score,
  }
  fetch(ajaxURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("ajax-msg").value = data.msg;
    });
}

window.addEventListener("load", (e) => {
  // Start section elements
  const startSection = document.getElementById("start");
  const operationSelect = document.getElementById("operation");
  const maxNumInput = document.getElementById("max-number");
  const go = document.getElementById("btn-go");
  const playTimeSpan = document.getElementById("playtime");

  // Play section elements
  const playSection = document.getElementById("play");
  const operationDisplay = document.getElementById("operation-display");
  const problemDisplay = document.getElementById("problem");
  const solutionInput = document.getElementById("solution");
  const numberPad = document.getElementById("number-pad");
  const numPadButtons = document.getElementsByClassName("button");
  const scoreboard = document.getElementById("scoreboard");
  const scoreOutput = document.querySelector("#scoreboard output");
  const timeLeftDiv = document.getElementById("time-left");
  const timeLeft = document.querySelector("#time-left output");

  // Result section elements
  const resultDiv = document.getElementById("result");
  const finalScore = document.getElementById("final-score");
  const playAgain = document.getElementById("btn-play-again");

  const PLAYTIME = 50;
  playTimeSpan.innerHTML = PLAYTIME;

  let operation = operationSelect.value;
  let maxNum = maxNumInput.value;

  go.addEventListener("click", (e) => {
    operation = operationSelect.value;
    maxNum = maxNumInput.value;
    play(operation, maxNum, PLAYTIME);
  });

  playAgain.addEventListener("click", (e) => {
    start();
  });

  for (btn of numPadButtons) {
    btn.addEventListener("click", (e) => {
      const btnClicked = e.target;
      if (btnClicked.id === "clear") {
        solutionInput.value = "";
      } else {
        solutionInput.value += btnClicked.innerHTML;
      }

      if (Number(solutionInput.value) === problem.a) {
        problem = generateProblem(operation, maxNum);
        problemDisplay.innerHTML = problem.q;
        solutionInput.value = "";
        scoreOutput.innerHTML = String(Number(scoreOutput.innerHTML) + 1);
      }
    });
  }

  function start() {
    startSection.style.display = "block";
    playSection.style.display = "none";
    problemDisplay.style.display = "block";
    solutionInput.style.display = "inline";
    solutionInput.value = "";
    numberPad.style.display = "block";
    scoreboard.style.display = "block";
    timeLeftDiv.style.display = "block";
    resultDiv.style.display = "none";
    scoreOutput.innerHTML = "0";
  }

  start();

  function timeUp(score) {
    problemDisplay.style.display = "none";
    solutionInput.style.display = "none";
    numberPad.style.display = "none";
    scoreboard.style.display = "none";
    timeLeftDiv.style.display = "none";
    resultDiv.style.display = "block";
    finalScore.innerHTML = score;
  }

  function play(operation, maxNum, time) {
    playSection.style.display = "block";
    startSection.style.display = "none";
    solutionInput.focus();
    timeLeft.innerHTML = time;
    operationDisplay.innerHTML = operation.toUpperCase();

    const interval = setInterval(() => {
      timeLeft.innerHTML = String(Number(timeLeft.innerHTML) - 1);
      if (Number(timeLeft.innerHTML) === 0) {
        const score = Number(scoreOutput.innerHTML);
        timeUp(scoreOutput.innerHTML);
        clearInterval(interval);
        saveScore(operation, maxNum, score);
      }
    }, 1000);

    let problem = generateProblem(operation, maxNum);
    problemDisplay.innerHTML = problem.q;

    for (btn of numPadButtons) {
      btn.addEventListener("click", (e) => {
        if (Number(solutionInput.value) === problem.a) {
          problem = generateProblem(operation, maxNum);
          problemDisplay.innerHTML = problem.q;
          solutionInput.value = "";
          scoreOutput.innerHTML = String(Number(scoreOutput.innerHTML) + 1);
        }
      });
    }

    solutionInput.addEventListener("input", (e) => {
      if (Number(solutionInput.value) === problem.a) {
        problem = generateProblem(operation, maxNum);
        problemDisplay.innerHTML = problem.q;
        solutionInput.value = "";
        scoreOutput.innerHTML = String(Number(scoreOutput.innerHTML) + 1);
      }
    });
  }
});