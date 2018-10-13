<template>
  <div>
    <b-alert show>Default Alert</b-alert>
    {{message}}
  </div>
</template>

<script>
  export default {
    data: function () {
      return {
        message: "hello world"
      }
    }
  }
</script>

<style scoped>
</style>
