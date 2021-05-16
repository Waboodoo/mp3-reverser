<template>
  <div class="error-message">{{ message }}</div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: true,
    }
  }
}
</script>

<style scoped lang="sass">
.error-message
  padding: 10px 20px
  color: #d25e5e
</style>