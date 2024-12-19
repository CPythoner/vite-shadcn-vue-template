<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 左右布局容器 -->
    <div class="flex">
      <!-- 左侧：播放器 -->
      <div class="w-1/2 p-8">
        <!-- 返回按钮 -->
        <button
          @click="router.back()"
          class="flex items-center text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft class="w-5 h-5 mr-2" />
          Back to Episodes
        </button>

        <!-- 标题和时间 -->
        <div class="flex gap-6 mb-8">
          <!-- 封面图片 -->
          <img
            :src="coverUrl"
            :alt="episode?.title"
            class="w-32 h-32 object-cover rounded-lg shadow-sm flex-shrink-0"
          />
          <!-- 标题和信息 -->
          <div>
            <h1 class="text-2xl font-bold mb-2">{{ episode?.title }}</h1>
            <p class="text-gray-500">
              {{ new Date(episode?.published_at || '').toLocaleDateString() }}
            </p>
            <p class="text-gray-600 mt-4 line-clamp-2">{{ episode?.description }}</p>
          </div>
        </div>

        <!-- 播放器卡片 -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <!-- 进度条和时间 -->
          <div class="flex items-center gap-4 mb-4">
            <span class="text-sm text-gray-500 w-12">{{ formatTime(currentTime) }}</span>
            <div class="flex-1 relative h-1 bg-gray-200 rounded cursor-pointer" @click="onProgressClick">
              <div
                class="absolute h-full bg-blue-500 rounded"
                :style="{ width: `${(currentTime / duration) * 100}%` }"
              ></div>
            </div>
            <span class="text-sm text-gray-500 w-12">{{ formatTime(duration) }}</span>
          </div>

          <!-- 播放控制 -->
          <div class="flex items-center justify-between">
            <!-- 左侧：播放控制 -->
            <div class="flex items-center gap-4">
              <button
                class="w-8 h-8 flex items-center justify-center text-gray-600 hover:text-gray-900"
                @click="togglePlay"
              >
                <Play v-if="!isPlaying" class="w-5 h-5" />
                <Pause v-else class="w-5 h-5" />
              </button>
              <select
                v-model="playbackRate"
                @change="changePlaybackRate"
                class="text-sm border rounded px-2 py-1"
              >
                <option value="1">1x</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
                <option value="2">2x</option>
              </select>
            </div>

            <!-- 右侧：音量控制 -->
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

        <!-- 完整描述 -->
        <div class="mt-8 bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold mb-4">关于本集</h2>
          <p class="text-gray-600">{{ episode?.description }}</p>
        </div>
      </div>

      <!-- 右侧：字幕 -->
      <div class="w-1/2 border-l border-gray-200 min-h-screen">
        <div class="p-8">
          <h2 class="text-xl font-semibold mb-6">Transcript</h2>
          <div class="space-y-4">
            <div
              v-for="segment in transcript"
              :key="segment.start_time"
              :class="{
                'p-4 rounded transition-colors cursor-pointer': true,
                'bg-blue-50': isCurrentSegment(segment),
                'hover:bg-gray-50': !isCurrentSegment(segment)
              }"
              @click="seekTo(segment.start_time)"
            >
              <p class="text-gray-900">{{ segment.text }}</p>
              <span class="text-sm text-gray-500">{{ formatTime(segment.start_time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PodcastAPI } from '@/lib/api'
import type { Episode, Podcast } from '@/lib/types'
import {
  ArrowLeft,
  Settings,
  Menu,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  FileText,
  Loader2,
  AlertCircle
} from 'lucide-vue-next'

interface TranscriptSegment {
  start_time: number
  end_time: number
  text: string
}

const route = useRoute()
const router = useRouter()
const api = new PodcastAPI()

const episode = ref<Episode | null>(null)
const podcast = ref<Podcast | null>(null)
const transcript = ref<TranscriptSegment[]>([])
const loading = ref(false)
const error = ref('')

const audioPlayer = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref('1')
const volume = ref(1)

// 计算属性：获取要显示的封面
const coverUrl = computed(() => {
  return episode.value?.cover_url || podcast.value?.cover_url
})

// 加载剧集和字幕
async function loadEpisodeAndTranscript() {
  loading.value = true
  error.value = ''
  try {
    const episodeId = parseInt(route.params.id as string)
    episode.value = await api.getEpisode(episodeId)
    // 加载播客信息
    if (episode.value) {
      podcast.value = await api.getPodcast(episode.value.podcast_id)
    }
    // TODO: 加载字幕
    // transcript.value = await api.getTranscript(episodeId)
  } catch (e) {
    error.value = '加载数据失败'
    console.error(e)
  } finally {
    loading.value = false
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
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 判断是否是当前播放的字幕段
function isCurrentSegment(segment: TranscriptSegment): boolean {
  return currentTime.value >= segment.start_time && currentTime.value < segment.end_time
}

// 跳转到指定时间
function seekTo(time: number) {
  if (!audioPlayer.value) return
  audioPlayer.value.currentTime = time
  if (!isPlaying.value) {
    audioPlayer.value.play()
  }
}

// 键盘快捷键
function handleKeyPress(event: KeyboardEvent) {
  switch (event.code) {
    case 'Space':
      event.preventDefault()
      togglePlay()
      break
    case 'ArrowLeft':
      skipBackward()
      break
    case 'ArrowRight':
      skipForward()
      break
  }
}

// 点击进度条跳转
function onProgressClick(event: MouseEvent) {
  const progressBar = event.currentTarget as HTMLElement
  const rect = progressBar.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  if (audioPlayer.value) {
    audioPlayer.value.currentTime = percent * duration.value
  }
}

onMounted(() => {
  loadEpisodeAndTranscript()
  window.addEventListener('keydown', handleKeyPress)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyPress)
})
</script>
