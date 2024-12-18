<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-3xl mx-auto">
        <!-- 返回按钮 -->
        <button
          @click="router.back()"
          class="mb-6 flex items-center text-gray-600 hover:text-gray-900"
        >
          <span class="mr-2">←</span> Back to Episodes
        </button>

        <!-- 剧集信息 -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h1 class="text-2xl font-bold mb-2">{{ episode?.title }}</h1>
          <p class="text-gray-600 mb-4">{{ episode?.date }}</p>
          <p class="text-gray-700 mb-6">{{ episode?.description }}</p>
        </div>

        <!-- 音频播放器 -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="mb-4">
            <audio
              ref="audioPlayer"
              :src="episode?.audioUrl"
              @timeupdate="onTimeUpdate"
              class="w-full"
            />
          </div>

          <!-- 播放控制 -->
          <div class="flex items-center gap-4">
            <button
              @click="togglePlay"
              class="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700"
            >
              {{ isPlaying ? '⏸' : '▶' }}
            </button>

            <!-- 进度条 -->
            <div class="flex-1">
              <input
                type="range"
                min="0"
                :max="duration"
                v-model="currentTime"
                @input="seekAudio"
                class="w-full"
              />
              <div class="flex justify-between text-sm text-gray-500">
                <span>{{ formatTime(currentTime) }}</span>
                <span>{{ formatTime(duration) }}</span>
              </div>
            </div>

            <!-- 播放速度 -->
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

        <!-- 字幕区域 -->
        <div class="bg-white rounded-lg shadow-lg p-6 mt-6">
          <h2 class="text-xl font-bold mb-4">Transcript</h2>
          <div class="space-y-4 text-gray-700">
            <p class="leading-relaxed">
              [00:00] Welcome to today's episode...
            </p>
            <p class="leading-relaxed">
              [00:15] Today we're going to talk about...
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const audioPlayer = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref(1)

// 获取剧集数据
const episode = ref({
  id: route.params.id,
  title: "English Listening - Techniques For Learning Vocabulary",
  date: "December 16, 2024",
  description: "Practice your English listening as I talk about some techniques for learning vocabulary.",
  audioUrl: "https://dts.podtrac.com/redirect.mp3/chrt.fm/track/G8F1AF/traffic.megaphone.fm/SONORO7201496122.mp3",
  transcriptUrl: "https://drive.google.com/file/d/1b8lSjpKxbcRWJS-JOJAoK0DKm4Y97UZI/view"
})

// 播放控制
const togglePlay = () => {
  if (!audioPlayer.value) return

  if (isPlaying.value) {
    audioPlayer.value.pause()
  } else {
    audioPlayer.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const onTimeUpdate = () => {
  if (!audioPlayer.value) return
  currentTime.value = audioPlayer.value.currentTime
  duration.value = audioPlayer.value.duration
}

const seekAudio = () => {
  if (!audioPlayer.value) return
  audioPlayer.value.currentTime = currentTime.value
}

const changePlaybackRate = () => {
  if (!audioPlayer.value) return
  audioPlayer.value.playbackRate = Number(playbackRate.value)
}

// 格式化时间
const formatTime = (time: number) => {
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

onMounted(() => {
  // 这里可以根据 route.params.id 获取具体剧集数据
})
</script>
