<template>
  <strong>Score: {{score}}</strong>
</template>

<script>
  export default {
    name: 'Score',
    props: {
      score: Number,
    }
  }
</script>