<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 播客信息 -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h1 class="text-3xl font-bold mb-4">英语新闻早餐 #123</h1>
      <div class="flex gap-4 mb-4">
        <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded">初级</span>
        <span class="bg-green-100 text-green-800 px-3 py-1 rounded">英语</span>
      </div>
      <p class="text-gray-600 mb-4">
        本期我们将讨论最新的国际新闻，包括...
      </p>
    </div>

    <!-- 音频播放器 -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <audio
        ref="audioPlayer"
        src="podcast-url.mp3"
        @timeupdate="onTimeUpdate"
      />
      <div class="flex items-center gap-4 mb-4">
        <button
          @click="togglePlay"
          class="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center"
        >
          {{ isPlaying ? '⏸' : '▶' }}
        </button>
        <div class="flex-1">
          <input
            type="range"
            min="0"
            max="100"
            v-model="currentTime"
            @input="seekAudio"
            class="w-full"
          />
        </div>
        <select
          v-model="playbackRate"
          @change="changePlaybackRate"
          class="px-2 py-1 border rounded"
        >
          <option value="0.75">0.75x</option>
          <option value="1">1x</option>
          <option value="1.25">1.25x</option>
          <option value="1.5">1.5x</option>
        </select>
      </div>
    </div>

    <!-- 字幕和文本 -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="mb-4">
        <h3 class="text-xl font-semibold mb-2">字幕</h3>
        <div class="bg-gray-50 p-4 rounded">
          <p class="mb-2">
            [00:00] Welcome to today's English news podcast...
          </p>
          <p class="mb-2">
            [00:15] Our first story today is about...
          </p>
        </div>
      </div>
    </div>

    <!-- 生词本 -->
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h3 class="text-xl font-semibold mb-4">生词本</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <span class="font-medium">vocabulary</span>
            <span class="text-gray-500 ml-2">[vəˈkæbjələri]</span>
          </div>
          <button class="text-blue-600">添加到生词本</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const audioPlayer = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const playbackRate = ref(1)

const togglePlay = () => {
  if (isPlaying.value) {
    audioPlayer.value.pause()
  } else {
    audioPlayer.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const onTimeUpdate = (e) => {
  currentTime.value = e.target.currentTime
}

const seekAudio = () => {
  audioPlayer.value.currentTime = currentTime.value
}

const changePlaybackRate = () => {
  audioPlayer.value.playbackRate = playbackRate.value
}
</script>
