<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- 主要内容区域 -->
    <div class="flex flex-col lg:flex-row flex-1 pb-[200px]">
      <!-- 左侧：播放器 -->
      <div class="w-full lg:w-2/5 p-4 lg:p-8 lg:sticky lg:top-0 lg:h-screen overflow-y-auto">
        <div class="lg:flex lg:flex-col lg:h-full lg:max-w-[400px] lg:mx-auto lg:min-h-[600px]">
          <!-- 返回按钮 -->
          <button
            @click="router.back()"
            class="flex items-center text-gray-600 hover:text-gray-900 mb-6 lg:mb-4"
          >
            <ArrowLeft class="w-5 h-5 mr-2" />
            Back to Episodes
          </button>

          <!-- 封面和标题信息 -->
          <div class="flex flex-col gap-4 lg:gap-6 lg:flex-1 lg:items-center lg:justify-center">
            <!-- 封面图片 -->
            <img
              :src="coverUrl"
              :alt="episode?.title"
              class="w-full max-w-[200px] aspect-square object-cover rounded-lg shadow-sm mx-auto"
            />
            <!-- 标题和信息 -->
            <div class="text-center max-w-full">
              <p class="text-sm text-gray-500 mb-1">Episode {{ episode?.episode_number }}</p>
              <h1 class="text-xl lg:text-2xl font-bold mb-2 break-words">{{ episode?.title }}</h1>
              <p class="text-gray-500">
                {{ new Date(episode?.published_at || '').toLocaleDateString() }}
              </p>
              <p class="text-gray-600 mt-2 text-sm lg:text-base break-words line-clamp-4 lg:line-clamp-none">
                {{ episode?.description }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：字幕 -->
      <div class="w-full lg:w-3/5 border-t lg:border-t-0 lg:border-l border-gray-200 flex flex-col flex-1">
        <div class="p-8 flex-1 flex flex-col">
          <h2 class="text-xl font-semibold mb-6">Transcript</h2>
          <div
            class="space-y-3 flex-1 overflow-y-auto px-2"
            ref="subtitlesContainer"
          >
            <div
              v-for="subtitle in subtitles"
              :key="`${subtitle.start_time}-${subtitle.end_time}`"
              :ref="el => { if (el) subtitleRefs[subtitle.start_time] = el }"
              :class="{
                'flex gap-4 py-2 transition-all duration-300 cursor-pointer': true,
                'text-base opacity-70': !isCurrentSubtitle(subtitle),
                'text-lg font-medium': isCurrentSubtitle(subtitle)
              }"
              @click="seekTo(subtitle.start_time)"
            >
              <span class="text-gray-400 w-12 flex-shrink-0">
                {{ formatTime(subtitle.start_time) }}
              </span>
              <div class="flex-1">
                <p class="text-gray-900">{{ subtitle.text }}</p>
                <p v-if="subtitle.translation" class="text-gray-500 mt-1">
                  {{ subtitle.translation }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 固定在底部的播放器 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg">
      <div class="max-w-screen-2xl mx-auto px-4">
        <!-- 播放器卡片 -->
        <div class="py-3">
          <!-- 播放控制栏 -->
          <div class="flex items-center gap-4 mb-3">
            <!-- 左侧：播放按钮 -->
            <button
              class="w-8 h-8 flex items-center justify-center text-gray-600 hover:text-gray-900"
              @click="togglePlay"
            >
              <Play v-if="!isPlaying" class="w-5 h-5" />
              <Pause v-else class="w-5 h-5" />
            </button>

            <!-- 时间显示 -->
            <span class="text-sm text-gray-500 w-12">{{ formatTime(currentTime) }}</span>

            <!-- 中间：进度条 -->
            <div
              class="flex-1 relative h-1 bg-gray-200 rounded cursor-pointer"
              @click="onProgressClick"
              ref="progressBar"
            >
              <div
                class="absolute h-full bg-blue-500 rounded"
                :style="{ width: `${(currentTime / duration) * 100}%` }"
              ></div>
            </div>

            <!-- 总时长 -->
            <span class="text-sm text-gray-500 w-12">{{ formatTime(duration) }}</span>

            <!-- 右侧：倍速和音量控制 -->
            <select
              v-model="playbackRate"
              @change="changePlaybackRate"
              class="text-sm border rounded px-2 py-1"
            >
              <option value="0.75">0.75x</option>
              <option value="1">1x</option>
              <option value="1.25">1.25x</option>
              <option value="1.5">1.5x</option>
              <option value="2">2x</option>
            </select>

            <div class="flex items-center gap-2">
              <Volume2 class="w-4 h-4 text-gray-600" />
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                v-model="volume"
                @input="changeVolume"
                class="w-20"
              />
            </div>
          </div>

          <!-- 隐藏的音频元素 -->
          <audio
            ref="audioPlayer"
            :src="episode?.audio_url"
            @timeupdate="onTimeUpdate"
            @loadedmetadata="onMetadataLoaded"
            @play="isPlaying = true"
            @pause="isPlaying = false"
            @ended="isPlaying = false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PodcastAPI } from '@/lib/api'
import type { Episode } from '@/lib/types'
import {
  ArrowLeft,
  Play,
  Pause,
  Volume2,
} from 'lucide-vue-next'

interface Subtitle {
  start_time: number
  end_time: number
  text: string
  translation?: string
}

const route = useRoute()
const router = useRouter()
const api = new PodcastAPI()

const episode = ref<Episode | null>(null)
const subtitles = ref<Subtitle[]>([])
const subtitleRefs = ref<Record<number, HTMLElement>>({})
const subtitlesContainer = ref<HTMLElement | null>(null)

const audioPlayer = ref<HTMLAudioElement | null>(null)
const progressBar = ref<HTMLElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref('1')
const volume = ref(1)

const coverUrl = computed(() => {
  return episode.value?.cover_url || episode.value?.podcast?.cover_url || '/default-cover.jpg'
})

// 加载剧集和字幕
async function loadEpisodeAndSubtitles() {
  try {
    const episodeId = parseInt(route.params.id as string)
    const [episodeData, subtitlesData] = await Promise.all([
      api.getEpisode(episodeId),
      api.getEpisodeSubtitles(episodeId)
    ])
    episode.value = episodeData
    subtitles.value = subtitlesData.map(subtitle => ({
      ...subtitle,
      start_time: Number(subtitle.start_time),
      end_time: Number(subtitle.end_time)
    }))
  } catch (e) {
    console.error(e)
  }
}

// 播放控制
function togglePlay() {
  if (!audioPlayer.value) return
  if (isPlaying.value) {
    audioPlayer.value.pause()
  } else {
    audioPlayer.value.play()
  }
}

// 更新播放进度
function onTimeUpdate() {
  if (!audioPlayer.value) return
  currentTime.value = audioPlayer.value.currentTime
  scrollToCurrentSubtitle()
}

// 音频加载完成
function onMetadataLoaded() {
  if (!audioPlayer.value) return
  duration.value = audioPlayer.value.duration
}

// 更改播放速度
function changePlaybackRate() {
  if (!audioPlayer.value) return
  audioPlayer.value.playbackRate = Number(playbackRate.value)
}

// 更改音量
function changeVolume() {
  if (!audioPlayer.value) return
  audioPlayer.value.volume = Number(volume.value)
}

// 格式化时间
function formatTime(seconds: number): string {
  const validSeconds = Number(seconds)
  if (isNaN(validSeconds)) {
    console.error('Invalid seconds value:', seconds)
    return '0:00'
  }
  const minutes = Math.floor(validSeconds / 60)
  const remainingSeconds = Math.floor(validSeconds % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 判断是否是当前字幕
function isCurrentSubtitle(subtitle: Subtitle): boolean {
  return currentTime.value >= subtitle.start_time && currentTime.value < subtitle.end_time
}

// 跳转到指定时间
function seekTo(time: number) {
  if (!audioPlayer.value) return
  const validTime = Number(time)
  if (isNaN(validTime)) {
    console.error('Invalid time value:', time)
    return
  }
  audioPlayer.value.currentTime = validTime
  if (!isPlaying.value) {
    audioPlayer.value.play()
  }
}

// 点击进度条跳转
function onProgressClick(event: MouseEvent) {
  if (!progressBar.value || !audioPlayer.value) return
  const rect = progressBar.value.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  audioPlayer.value.currentTime = percent * duration.value
}

// 滚动到当前字幕
function scrollToCurrentSubtitle() {
  const currentSubtitle = subtitles.value.find(subtitle => isCurrentSubtitle(subtitle))
  if (currentSubtitle && subtitlesContainer.value) {
    const element = subtitleRefs.value[currentSubtitle.start_time]
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }
}

// 键盘快捷键
function handleKeyPress(event: KeyboardEvent) {
  if (!audioPlayer.value) return

  switch (event.code) {
    case 'Space':
      event.preventDefault()
      togglePlay()
      break
    case 'ArrowLeft':
      audioPlayer.value.currentTime -= 5
      break
    case 'ArrowRight':
      audioPlayer.value.currentTime += 5
      break
  }
}

onMounted(() => {
  loadEpisodeAndSubtitles()
  window.addEventListener('keydown', handleKeyPress)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyPress)
})
</script>
