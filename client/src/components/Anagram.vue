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
            <div class="huge">{{score}}</div>
            <strong class="big">Anagrams</strong>
            <button class="btn btn-primary form-control m-1" @click="restart()">
              Play Again with Same Settings
            </button>
            <button class="btn btn-secondary form-control m-1" @click="config()">
              Change Settings
            </button>
          </div>
        </template>
      </transition>
      <transition name="slide-right">
        <template v-if="timeLeft > 0">
          <div>
            <div class="row border-bottom mt-5" id="scoreboard">
              <div class="col px-3 text-left">
                <Score :score="score" />
              </div>
              <div class="col px-3 text-right">
                <Timer :timeLeft="timeLeft" />
              </div>
            </div>
            <div :class="equationClass" id="equation">
              <Word :word="wordQuestion" />
            </div>
            <div class="row">
              <div class="col">
                <input v-model="input" placeholder="type here">
              </div>
            </div>
            <ol>
              <li v-for="item in finishedWords" :key="item">{{item}}</li>
            </ol>
          </div>
        </template>
      </transition>
    </div>
  </main>
</template>

<script>
  import SelectInput from './SelectInput';
  import PlayButton from './PlayButton';
  import Score from './Score'
  import Timer from './Timer'
  import Word from './Word'
  import {
    anagrams
  } from '../helpers/anagrams'
  import {
    getRandomInt
  } from '../helpers/helpers'


  export default {
    name: 'Anagram',
    components: {
      SelectInput,
      PlayButton,
      Score,
      Timer,
      Word,
    },
    data: function() {
      return {
        wordLength: '5',
        screen: 'config',
        buttons: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        input: '',
        answered: false,
        score: 0,
        gameLength: 1000,
        timeLeft: 0,
        answerSetIndex: 0,
        finishedWords: []
      }
    },
    methods: {
      config() {
        this.screen = "config";
      },
      play() {
        this.screen = "play";
        this.startTimer();
      },
      restart() {
        this.score = 0;
        this.startTimer();
        this.newWord();
      },
      // setInput(value) {
      //   this.input += String(value);
      //   this.input = String(Number(this.input));
      //   this.answered = this.checkAnswer(this.input, this.operation, this.operands);

      //   if (this.answered) {
      //     setTimeout(this.newWord, 300);
      //     this.score++;
      //   }
      // },
      clear() {
        this.input = '';
      },
      newWord() {
        this.input = '';
        this.answered = false;
        this.getAnswerSetIndex
      },
      checkAnswer(userAnswer, wordQuestion) {
        if (!userAnswer) {
          return false; // User hasn't answered
        } else if (userAnswer == wordQuestion) {
          return false; // same as prompted word
        } else if (this.finishedWords.includes(userAnswer)) {
          return false; // already gotten
        } else if (this.answerSet.includes(userAnswer)) {
          this.finishedWords.push(userAnswer) // add to previously gotten answers
          return true;
        }
      },
      startTimer() {
        window.addEventListener('keyup', this.handleKeyUp)
        this.timeLeft = this.gameLength;
        if (this.timeLeft > 0) {
          this.timer = setInterval(() => {
            this.timeLeft--;
            if (this.timeLeft === 0) {
              clearInterval(this.timer);
              window.removeEventListener('keyup', this.handleKeyUp)
            }
          }, 1000)
        }
      },
      handleKeyUp(e) {
        e.preventDefault(); // prevent the normal behavior of the key
        if (e.keyCode === 13) { // Enter
          this.answered = this.checkAnswer(this.input, this.wordQuestion)

          if (this.answered) {
            setTimeout(this.newWord, 300);
            this.score++;
          }
        }
      },
      getAnswerSetIndex() { // computes random index for set of anagrams with given word length
        var setLength = anagrams[this.wordLength].length
        this.answerSetIndex = getRandomInt(setLength)
      },
    },
    computed: {
      numbers: function() {
        const numbers = [];
        for (let number = 5; number <= 8; number++) {
          numbers.push([number, number])
        }
        return numbers;
      },
      wordQuestion: function() {
        var answerIndex = getRandomInt(this.answerSet.length)
        return this.answerSet[answerIndex]
      },
      answerSet: function() {
        var answerSet = anagrams[this.wordLength][this.answerSetIndex]
        return answerSet
      }
      // equationClass: function() {
      //   if (this.answered) {
      //     return 'row text-primary my-2 fade';
      //   } else {
      //     return 'row text-seconday my-2';
      //   }
      // }
    },
  }
</script>

<style>
  #main-container {
    margin: auto;
    width: 380px;
  }

  button.number-button {
    border-radius: .25em;
    font-size: 3em;
    height: 2em;
    margin: .1em;
    text-align: center;
    width: 2em;
  }

  #clear-button {
    border-radius: .25em;
    font-size: 3em;
    height: 2em;
    margin: .1em;
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
    transition: opacity .5s;
  }

  .slide-leave-to {
    transform: translate(100%, 0);
    opacity: 0;
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
    transition: opacity .5s;
  }

  .slide-right-leave-to {
    transform: translate(-100%, 0);
    opacity: 0;
  }
</style>