<template>
  <div class="options clearfix">
    <div class="checkbox clearfix">
      <input type="checkbox" name="opt_reverse" id="opt_reverse" v-model="reverse">
      <div></div>
      <label for="opt_reverse">Reverse</label>
    </div>

    <div class="select clearfix">
      <div>
        <span></span>
        <select name="opt_speed" id="opt_speed" v-model="speed">
          <option value="50">0.5×</option>
          <option value="60">0.6×</option>
          <option value="70">0.7×</option>
          <option value="80">0.8×</option>
          <option value="90">0.9×</option>
          <option value="100" selected>1.0×</option>
          <option value="110">1.1×</option>
          <option value="120">1.2×</option>
          <option value="130">1.3×</option>
          <option value="140">1.4×</option>
          <option value="150">1.5×</option>
          <option value="160">1.6×</option>
          <option value="170">1.7×</option>
          <option value="180">1.8×</option>
          <option value="190">1.9×</option>
          <option value="200">2.0×</option>
        </select>
      </div>
      <label for="opt_speed">Change Speed</label>
    </div>

    <div class="checkbox clearfix" v-if="showKeepPitchOption">
      <input type="checkbox" name="opt_pitch" id="opt_pitch" v-model="keepPitch">
      <div></div>
      <label for="opt_pitch">Keep Pitch</label>
    </div>

    <div class="checkbox clearfix">
      <input type="checkbox" name="opt_stereo_shift" id="opt_stereo_shift" v-model="stereoShift">
      <div></div>
      <label for="opt_stereo_shift">Stereo Shift</label>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reverse: true,
      speed: '100',
      keepPitch: true,
      stereoShift: false,
    };
  },
  computed: {
    showKeepPitchOption() {
      return this.speed !== '100';
    },
  },
  methods: {
    getOptions() {
      return {
        reverse: this.reverse,
        speed: Number.parseInt(this.speed, 10),
        keepPitch: this.keepPitch,
        stereoShift: this.stereoShift ? 2 : 0,
      };
    }
  },
}
</script>

<style scoped lang="sass">
.options
  margin: 10px 20px

.checkbox, .select
  float: left
  margin-right: 40px
  margin-top: 10px
  position: relative

.select > label,
.checkbox > label
  line-height: 26px
  height: 26px
  vertical-align: middle
  float: left
  cursor: pointer

.checkbox > input
  width: 26px
  height: 26px
  opacity: 0
  position: absolute
  top: 0
  left: 0
  cursor: pointer

.checkbox > div
  float: left
  margin-right: 10px
  width: 26px
  height: 26px
  border-radius: 5px
  border: 3px solid #497198
  background-repeat: no-repeat
  background-position: center

.checkbox > input:checked + div
  background-image: url('~@/assets/tick.png')

.select > div
  border-radius: 5px
  border: 3px solid #497198
  float: left
  margin-right: 10px

.select > div > select
  height: 20px
  display: block
  cursor: pointer
</style>