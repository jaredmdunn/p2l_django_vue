<template>
  <div class="row mx-1 my-3">
    <label class="col font-weight-bold" font-weight-bold :for="id">{{label}}</label>
    <select class="form-control col" :id="id" :value="currentValue" @input="$emit('input',$event.target.value)">
      <option v-for="option in options" :key="option[1]" :value="option[1]">{{option[0]}}</option>
    </select>
  </div>
</template>

<script>
  export default {
    name: 'SelectInput',
    props: {
      id: String,
      label: String,
      options: Array,
      currentValue: String
    },
    data: function() {
      return {}
    }
  }
</script>