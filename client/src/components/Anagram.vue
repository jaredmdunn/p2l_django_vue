<template>
  <main id="main-container">
    <div v-if="screen === 'config'" id="config-container">
      <h1>Anagram Hunt</h1>
      <SelectInput :currentValue="wordLength" label="Word Length" id="word-length" v-model="wordLength" :options="numbers" />
      <PlayButton @play-button-click="play" />
    </div>
    <div v-else-if="screen === 'play'" id="game-container" class="text-center">
      <transition name="slide">
        <template v-if="timeLeft === 0">
          <div>
            <h2>Time's Up!</h2>
            <strong class="big">You Got</strong>
            <div class="huge">{{ score }}</div>
            <strong class="big">Anagrams</strong>
            <div id="ajax-msg">{{ ajaxMsg }}</div>
            <button class="btn btn-primary form-control m-1" @click="play">
              Play Again with Same Settings
            </button>
            <button class="btn btn-secondary form-control m-1" @click="config">
              Change Settings
            </button>
          </div>
        </template>
      </transition>
      <transition name="slide-right">
        <template v-if="timeLeft > 0">
          <div>
            <div class="row border-bottom mt-5">
              <div class="col px-3 text-left">
                <Score :score="score" />
              </div>
              <div class="col px-3 text-right">
                <Timer :timeLeft="timeLeft" />
              </div>
            </div>
            <div>
              <Word :word="currentWordQuestion" />
            </div>
            <div class="row">
              <div class="col">
                <input v-model="input" placeholder="type here" />
              </div>
              <div class="col">
                <button @click="newWord()" class="btn btn-success">
                  New Word
                </button>
              </div>
            </div>
            <ol>
              <li v-for="item in finishedWords[this.answerSets.indexOf(this.currentAnswerSet)]" :key="item">
                {{ item }}
              </li>
            </ol>
          </div>
        </template>
      </transition>
    </div>
  </main>
</template>

<script>
  import SelectInput from "./SelectInput";
  import PlayButton from "./PlayButton";
  import Score from "./Score";
  import Timer from "./Timer";
  import Word from "./Word";
  import {
    anagrams
  } from "../helpers/anagrams";
  import {
    clone, shuffle
  } from "../helpers/helpers";

  export default {
    name: "Anagram",
    components: {
      SelectInput,
      PlayButton,
      Score,
      Timer,
      Word,
    },
    data: function() {
      return {
        ajaxMsg: "",
        ajaxURL: "/games/anagram-hunt/save-score/",
        anagramsCopy: clone(anagrams),
        answered: false, // only used in handleKeyUp and is recomputed every time
        answerSets: [],
        // gets the csrf token from the csrf cookie that is automatically set by Django
        csrfToken: document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken"))
          .split("=")[1],
        currentAnswerSet: [],
        currentWordQuestion: '',
        finishedWords: [],
        gameLength: 60,
        input: "",
        score: 0,
        screen: "config",
        timeLeft: 0,
        wordLength: "5",
        wordQuestions: [],
      };
    },
    methods: {
      /**
       * Sets the screen display to the config page before playing.
       */
      config() {
        this.screen = "config";
      },
      /**
       * Begins the game by setting the screen display to the play page and 
       * starting the timer.
       */
      play() {
        this.screen = "play";
        this.reset();
        shuffle(this.anagramsCopy[this.wordLength]) // randomize order of answer sets
        this.startTimer();
      },
      /**
       * Resets stored data to play another round.
       */
      reset() {
        this.anagramsCopy = clone(anagrams);
        this.input = "";
        this.answered = false;
        this.score = 0;
        this.answerSets = [];
        this.finishedWords = [];
        this.wordQuestions = [];
      },
      /**
       * Resets the input and answered data values after the user gets a 
       * correct anagram.
       */
      correctWord() {
        this.input = "";
        this.answered = false;
      },
      /**
       * Resets the input and answered data values and calls another function to
       * get a new answer set and word question.
       */
      newWord() {
        this.input = "";
        this.answered = false;
        this.setAnswerSetAndWordQuestion();
      },
      /**
       * Checks if the user has inputted a valid anagram for the current word
       * question.
       * @param {string} userAnswer - the user's inputted answer
       * @return {boolean} - true if userAnswer is a valid answer, and false
       * if not
       */
      checkAnswer(userAnswer) {
        if (!userAnswer) {
          return false; // user hasn't answered
        }
        if (this.currentAnswerSet.includes(userAnswer)) {
          let answerIndex = this.currentAnswerSet.indexOf(userAnswer);
          this.currentAnswerSet.splice(answerIndex, 1); // remove anagram from answer set
          if (this.finishedWords[this.answerSets.indexOf(this.currentAnswerSet)]) {
            this.finishedWords[this.answerSets.indexOf(this.currentAnswerSet)].push(userAnswer);
          } else {
            this.finishedWords[this.answerSets.indexOf(this.currentAnswerSet)] = [userAnswer];
          }
          return true;
        }
      },
      /**
       * Starts the timer and adds an event listener to monitor if the user
       * tries to submit an answer.
       */
      startTimer() {
        window.addEventListener("keyup", this.handleKeyUp);
        this.timeLeft = this.gameLength;
        this.setAnswerSetAndWordQuestion();
        if (this.timeLeft) {
          this.timer = setInterval(() => {
            this.timeLeft--;
            if (!this.timeLeft) {
              clearInterval(this.timer);
              window.removeEventListener("keyup", this.handleKeyUp);
              this.saveScore(this.wordLength, this.score);
            }
          }, 1000);
        }
      },
      /**
       * Monitors the user's keyboard input; if the user presses the Enter key,
       * checks for a valid answer and then advances to the next word and 
       * increases the score appropriately.
       * @param {event} e - the event generated by the user pressing a key
       */
      handleKeyUp(e) {
        e.preventDefault(); // prevent the normal behavior of the key
        if (e.keyCode === 13) { // Enter
          this.answered = this.checkAnswer(this.input.trim());
          if (this.answered) {
            if (!this.currentAnswerSet.length) { // when word is finished
              let answerSetIndex = this.answerSets.indexOf(this.currentAnswerSet);
              this.answerSets.splice(answerSetIndex, 1); // remove answer set from answer sets list
              this.wordQuestions.splice(answerSetIndex, 1); // remove word question from word questions list
              this.finishedWords.splice(answerSetIndex, 1);
              if (!this.answerSets.length && !this.anagramsCopy[this.wordLength].length) { // when finished with all words
                this.timeLeft = 1;
              } else {
                setTimeout(this.newWord(), 300);
              }
            } else {
              setTimeout(this.correctWord, 300);
            }
            this.score++;
          }
        }
      },
      /**
       * Sets the answer set and word question for the user when the game
       * starts, when the user finishes an answer set, and when the user clicks
       * the new word button. 
       */
      setAnswerSetAndWordQuestion() {
        if (this.anagramsCopy[this.wordLength].length) {
          let newAnswerSet = shuffle(this.anagramsCopy[this.wordLength].pop());
          this.answerSets.push(newAnswerSet);
          this.currentAnswerSet = newAnswerSet;

          let newWordQuestion = newAnswerSet.pop();
          this.wordQuestions.push(newWordQuestion);
          this.currentWordQuestion = newWordQuestion;
        } else {
          let oldIndex = this.answerSets.indexOf(this.currentAnswerSet);
          let newIndex = (oldIndex + 1) % this.answerSets.length;

          this.currentAnswerSet = this.answerSets[newIndex];
          this.currentWordQuestion = this.wordQuestions[newIndex];
        }
      },
      /**
       * Sends the user's score and wordLength param to the server. 
       * Then sets the ajaxMsg div to the reponse message.
       * 
       * @param {number} wordLength - the length of anagram the user chose
       * @param {number} score - the user's final score
       */
      saveScore(wordLength, score) {
        const data = {
          parameters: {
            "word-length": wordLength,
          },
          score: score,
        };
        fetch(this.ajaxURL, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.csrfToken,
            },
            body: JSON.stringify(data),
          })
          .then((response) => response.json())
          .then((data) => {
            this.ajaxMsg = data.msg;
          });
      },
    },
    computed: {
      // the possible word lengths
      numbers: function() {
        const numbers = [];
        for (let number = 5; number <= 8; number++) {
          numbers.push([number, number]);
        }
        return numbers;
      },
    },
  };
</script>

<style>
  #main-container {
    margin: auto;
    width: 380px;
  }

  button.number-button {
    border-radius: 0.25em;
    font-size: 3em;
    height: 2em;
    margin: 0.1em;
    text-align: center;
    width: 2em;
  }

  #clear-button {
    border-radius: 0.25em;
    font-size: 3em;
    height: 2em;
    margin: 0.1em;
    text-align: center;
    width: 4.2em;
  }

  #scoreboard {
    font-size: 1.5em;
  }

  .big {
    font-size: 1.5em;
  }

  .huge {
    font-size: 5em;
  }

  .slide.leave-active,
  .slide-enter-active {
    position: absolute;
    top: 56px;
    transition: 1s;
    width: 380px;
  }

  .slide-enter {
    transform: translate(-100%, 0);
    transition: opacity 0.5s;
  }

  .slide-leave-to {
    opacity: 0;
    transform: translate(100%, 0);
  }

  .slide-right-leave-active,
  .slide-right-enter-active {
    position: absolute;
    top: 56px;
    transition: 1s;
    width: 380px;
  }

  .slide-right-enter {
    transform: translate(100%, 0);
    transition: opacity 0.5s;
  }

  .slide-right-leave-to {
    opacity: 0;
    transform: translate(-100%, 0);
  }
</style>