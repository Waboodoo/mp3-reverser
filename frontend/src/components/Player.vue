<template>
  <div>
    <audio controls class="player">
      <source :src="url" type="audio/mp3">
    </audio>
  </div>
</template>

<script>
export default {
  props: {
    url: {
      type: String,
      required: true,
    },
  },
}
</script>

<style scoped lang="sass">
.player
  margin: 20px 0
  width: 100%
</style>
