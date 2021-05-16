<template>
  <div class="form">
    <div class="file-input-container" :class="{'has-file': !!selectedFile}">
      <label
          class="file-input-label button"
          for="audio-file"
      >
        Choose File
      </label>
      <div class="file-name-container">
        <input
            class="file-input"
            type="file"
            id="audio-file"
            accept="audio/*"
            @change="onFileSelected"
            :disabled="isInProgress"
        >
        <div class="file-name">
          <span>{{ fileName }}</span>
          <div
              class="progress-bar"
              :class="{'in-progress': isInProgress, 'complete': isDone, 'error': isError}"
          ></div>
        </div>
      </div>
      <button
          class="submit-button button"
          type="submit"
          @click="startUpload"
          :class="{visible: canUpload}"
      >
        Go!
      </button>
      <a
          :href="resultUrl"
          :download="fileName"
          class="download-button button"
          :class="{visible: !!resultUrl}"
      >Download</a>
    </div>
    <options v-show="canUpload" ref="options" />
    <error-message v-if="isError" :message="error" />
    <player
        v-if="resultUrl"
        :url="resultUrl"
        :file-name="fileName"
    />
  </div>
</template>

<script>
import APIClient from '@/api/APIClient';
import ErrorMessage from '@/components/ErrorMessage';
import Options from '@/components/Options';
import Player from '@/components/Player';

export default {
  components: {
    ErrorMessage,
    Options,
    Player,
  },
  data() {
    return {
      selectedFile: null,
      resultUrl: null,
      isInProgress: false,
      error: false,
    };
  },
  computed: {
    canUpload() {
      return !!this.selectedFile && !this.isInProgress && !this.isDone;
    },
    isDone() {
      return !!this.resultUrl;
    },
    isError() {
      return !!this.error;
    },
    fileName() {
      return this.selectedFile?.name;
    },
  },
  methods: {
    onFileSelected() {
      this.error = null;
      this.selectedFile = document.getElementById('audio-file').files[0];
      this.resultUrl = null;
    },
    async startUpload() {
      try {
        this.error = null;
        this.isInProgress = true;
        this.resultUrl = null;
        const options = this.$refs.options.getOptions();
        const client = new APIClient();
        const processedResult = await client.upload(this.selectedFile, options);
        this.resultUrl = processedResult.url;
      } catch (e) {
        this.onError();
      } finally {
        this.isInProgress = false;
      }
    },
    onError() {
      this.error = 'An error occurred. Please try again later or use a different file.';
    },
  },
}
</script>

<style scoped lang="sass">
.form
  padding: 20px 0

.button
  text-align: center
  border: none
  color: #FFFFFF
  border-radius: 20px
  background: #497198
  background: linear-gradient(to bottom,  #497198 35%,#29517a 62%)
  cursor: pointer
  font-size: 15px
  white-space: nowrap
  line-height: 40px
  height: 40px
  vertical-align: middle
  padding: 0 36px

  &:hover
    background: #4e79a3
    background: linear-gradient(to bottom,  #4e79a3 35%, #2f5c8a 62%)

.file-input-container
  position: relative
  display: flex
  justify-content: flex-start

.file-input-label
  .has-file &
    border-top-right-radius: 0
    border-bottom-right-radius: 0

.file-name-container
  flex-grow: 1
  overflow: hidden
  position: relative
  border-top-right-radius: 20px
  border-bottom-right-radius: 20px

  .file-input
    position: absolute
    top: 0
    left: 0
    width: 100%
    height: 100%
    opacity: 0
    z-index: 3

.file-name
  position: relative
  width: 0
  transition: width 0.8s ease-in-out
  border-top-right-radius: 20px
  border-bottom-right-radius: 20px
  background: #dcdcea
  background: linear-gradient(to bottom, #dcdcea 20%,#efefef 79%)

  span
    z-index: 2
    position: relative
    display: block
    padding: 0 20px
    overflow: hidden
    text-overflow: ellipsis
    white-space: nowrap
    height: 40px
    vertical-align: middle
    line-height: 40px
    color: #333333

  .progress-bar
    z-index: 1
    position: absolute
    left: 0
    top: 0
    width: 100%
    height: 100%
    opacity: 0
    background-image: url('~@/assets/bar.png')
    background-color: #6699cc
    background-repeat: repeat
    animation: progress 2.5s
    animation-iteration-count: infinite
    animation-timing-function: linear
    box-shadow: 0 0 10px rgba(0,0,0,0.8)
    transition: background-color 1s ease-in-out, opacity 1s ease-in-out

    &.in-progress
      opacity: 1

    &.complete
      opacity: 1
      background-color: #60E062
      animation-play-state: paused

    &.error
      opacity: 1
      background-color: #d25e5e
      animation-play-state: paused

  .has-file &
    width: 100%

@keyframes progress
  0%
    background-position: 0 0

  100%
    background-position: 55px 0

.submit-button
  display: none
  margin-left: 10px

  &.visible
    display: block

.download-button
  display: none
  margin-left: 10px

  &.visible
    display: block
</style>
