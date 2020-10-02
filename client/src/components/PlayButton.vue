<template>
  <div class="row mx-1 my-3">
    <button class="btn btn-primary form-control" 
      @click="$emit('play-button-click')">Play!</button>
  </div>
</template>

<script>
  export default {
    name: 'PlayButton'
  }
</script>