<template>
  <strong>Time Left: {{timeLeft}}</strong>
</template>

<script>
  export default {
    name: 'Timer',
    props: {
      timeLeft: Number,
    }
  }
</script>