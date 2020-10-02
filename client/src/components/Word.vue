<template>
  <div id="word">
    {{word}}
  </div>
</template>

<script>
  export default {
    name: 'Word',
    props: {
      word: String,
    }
  }
</script>
<style scoped>
  #word {
    font-size: 1.6em;
    margin: auto;
    width: 90%;
  }
</style>