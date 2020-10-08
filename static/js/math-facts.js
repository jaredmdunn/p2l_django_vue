/**
 * Generates a random integer between low and high
 * @param {number} low - the lowest number inclusive
 * @param {number} high - the highest number exclusive
 * @return {number} - a random integer
 */
function randInt(low, high) {
  const rndDec = Math.random();
  const rndInt = Math.floor(rndDec * (high - low + 1) + low);
  return rndInt;
}

/**
 * Generates a problem based on the selected operation and max number
 * @param {string} operation 
 * @param {number} maxNum 
 */
function generateProblem(operation, maxNum) {
  // initialize q (question) and a (answer)
  let q, a;
  // set maxNum to 20 if it is less than or equal to 0
  if (maxNum <= 0) maxNum = 20;
  // if operation is "addition"
  // generate a problem with addition
  if (operation === "addition") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(0, maxNum);
    q = String(num1) + " + " + String(num2);
    a = num1 + num2;
    // if operation is "subtraction"
    // generate a problem with subtraction
  } else if (operation === "subtraction") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(num1, maxNum);
    q = String(num2) + " - " + String(num1);
    a = num2 - num1;
    // if operation is "multiplication"
    // generate a problem with multiplication
  } else if (operation === "multiplication") {
    const num1 = randInt(0, maxNum);
    const num2 = randInt(0, maxNum);
    q = String(num1) + " x " + String(num2);
    a = num1 * num2;
    // if operation is "division"
    // generate a problem with division
  } else if (operation === "division") {
    const num1 = randInt(1, maxNum);
    const num2 = randInt(0, maxNum);
    const num3 = num1 * num2;
    q = String(num3) + " / " + String(num1);
    a = num2;
  }
  // return a JSON object with the question and answer
  return {
    "q": q,
    "a": a
  };
}

/**
 * Sends an Ajax request to the server to save the user's score
 * and returns a success message if successful
 * @param {string} operation - the operation selected by the user
 * @param {*} maxNum - the max number selected by the user
 * @param {*} score - the user's final score
 */
function saveScore(operation, maxNum, score) {
  // TODO: Discuss whether or not using the csrf input element is best practice for Ajax calls
  // Also discuss about getting the AjaxURL 
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
  // Create a JSON object that stores information 
  // on the user's parameters and score for the game
  const data = {
    "parameters": {
      "operation": operation,
      "max-number": maxNum,
    },
    "score": score,
  }
  // call fetch to send the data to the server
  fetch(ajaxURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    // if successful, set the ajax-msg output value to the return message
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

  // the game time
  const PLAYTIME = 30;
  playTimeSpan.innerHTML = PLAYTIME;

  // initialize operation and maxNum to the default values of the selects
  let operation = operationSelect.value;
  let maxNum = maxNumInput.value;

  // when the go button is clicked,
  // set operation and maxNum to the values selected by the user
  // and call play()
  go.addEventListener("click", (e) => {
    operation = operationSelect.value;
    maxNum = maxNumInput.value;
    play(operation, maxNum, PLAYTIME);
  });

  // when playAgain is clicked,
  // call start()
  playAgain.addEventListener("click", (e) => {
    start();
  });

  // add an event listener to each button in the number pad
  // so that when they are clicked they put the number 
  // into the solution input (except clear which clears the input)
  for (btn of numPadButtons) {
    btn.addEventListener("click", (e) => {
      const btnClicked = e.target;
      if (btnClicked.id === "clear") {
        solutionInput.value = "";
      } else {
        solutionInput.value += btnClicked.innerHTML;
      }
    });
  }

  /**
   * Display elements for the start screen, hides others
   */
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

  // call start() when the window loads
  start();

  /**
   * Displays elements for the time up screen, hides others
   * @param {number} score - the score the user got on the game
   */
  function timeUp(score) {
    problemDisplay.style.display = "none";
    solutionInput.style.display = "none";
    numberPad.style.display = "none";
    scoreboard.style.display = "none";
    timeLeftDiv.style.display = "none";
    resultDiv.style.display = "block";
    finalScore.innerHTML = score;
  }

  /**
   * Displays elements for the play screen, hides others.
   * Also, sets timer, sets first problem, 
   * adds event listeners to button pad clicks 
   * and changes to the solution input so that 
   * if the input value is the solution a new question is generated
   * 
   * @param {string} operation - the operation selected by the user
   * @param {number} maxNum - the max number selected by the user
   * @param {number} time - the game time
   */
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
        if (solutionInput.value === String(problem.a)) {
          problem = generateProblem(operation, maxNum);
          problemDisplay.innerHTML = problem.q;
          solutionInput.value = "";
          scoreOutput.innerHTML = String(Number(scoreOutput.innerHTML) + 1);
        }
      });
    }

    solutionInput.addEventListener("input", (e) => {
      if (solutionInput.value === String(problem.a)) {
        problem = generateProblem(operation, maxNum);
        problemDisplay.innerHTML = problem.q;
        solutionInput.value = "";
        scoreOutput.innerHTML = String(Number(scoreOutput.innerHTML) + 1);
      }
    });
  }
});