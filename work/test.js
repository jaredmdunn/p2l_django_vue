function randInt(low, high) {
  const rndDec = Math.random();
  return Math.floor(rndDec * (high - low + 1) + low);
}

function removeItem(arr, value) {
  // Removes first instance of value from arr and returns true if value existed.
  var index = arr.indexOf(value);
  if (index > -1) {
    arr.splice(index, 1);
    return true;
  }
  return false;
}

function shuffle(a) {
  var j, x, i;
  for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      x = a[i];
      a[i] = a[j];
      a[j] = x;
  }
  return a;
}


const origArray = [
  ["parroted", "predator", "prorated", "teardrop"],
  ["repaints", "painters", "pantries", "pertains"],
  ["restrain", "retrains", "strainer", "terrains", "trainers"],
  ["construe", "counters", "recounts", "trounces"]
];

// shuffle outer and inner arrays
let anagramSets = JSON.parse(JSON.stringify(origArray));
shuffle(anagramSets);
for (const anagramSet of anagramSets) {
  /* 
    Change each anagramSet to use the following structure:
    [wordToGuess, [unguessedWords], [guessedWords]]
  */
  shuffle(anagramSet);
  anagramSet[1] = anagramSet.slice(1); // anagrams to be guessed
  anagramSet[2] = []; // guessed anagrams
  anagramSet.length = 3; // truncate extra words
}

play(anagramSets);


function play(anagramSets, i=0) {
  const anagramSet = anagramSets[i % anagramSets.length];
  const anchorWord = anagramSet[0]; // get first element of array
  console.log(`ANCHOR WORD: ${anchorWord}. ANAGRAMS: ${anagramSet.slice(1)}`);
  
  r = randInt(0, anagramSet.length-1); // number of correct guesses
  console.log('CORRECT GUESSES:', r);

  // For each correct guess, remove one of the anagrams
  for (let i=0; i < r; i++) {
    // remove last word. In game, you could use removeItem to remove an item by value.
    anagramSet[2].push(anagramSet[1].pop());
  }
  console.log(`ANAGRAMS LEFT: ${anagramSet}`);
  console.log('-----------------------');
  
  // Record the number remaining before any are removed.
  let anagramSetsRemaining = anagramSets.length;

  // remove empty anagramSets (when the second element is an empty list). This is an easy way of
  // removing completed anagramSets without having to keep track of the index.
  anagramSets = anagramSets.filter(el => el[1].length);

  // If no anagram sets were removed, i should increment.
  // If a set was removed, i shouldn't change as every item after the removed
  // item will fall back one index.
  i = (anagramSetsRemaining === anagramSets.length) ? i+1 : i;

  // if any anagramSets remain, move to the next anagramSet.
  if (anagramSets.length) {
    play(anagramSets, i);
  } else {
    console.log('Game over!')
  }
}

console.log(anagramSets);