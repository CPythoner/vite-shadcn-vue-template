<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-8">
      加载中...
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="text-red-500 text-center py-8">
      {{ error }}
    </div>

    <!-- 播客详情 -->
    <div v-if="podcast" class="mb-8">
      <div class="flex flex-col md:flex-row gap-8">
        <!-- 封面图 -->
        <img
          :src="podcast.cover_url"
          :alt="podcast.title"
          class="w-full md:w-64 h-64 object-cover rounded-lg shadow-lg"
        />

        <!-- 播客信息 -->
        <div class="flex-1">
          <h1 class="text-3xl font-bold mb-4">{{ podcast.title }}</h1>
          <div class="flex gap-2 mb-4">
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
              {{ podcast.level }}
            </span>
            <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
              {{ podcast.category }}
            </span>
          </div>
          <p class="text-gray-600 mb-4">{{ podcast.description }}</p>
          <div class="flex items-center text-gray-500 text-sm">
            <span>{{ podcast.episode_count }}集</span>
            <span class="mx-2">·</span>
            <span>最近更新: {{ new Date(podcast.latest_episode_at).toLocaleDateString() }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 剧集列表 -->
    <div v-if="episodes.length > 0" class="space-y-4">
      <h2 class="text-2xl font-bold mb-6">所有剧集</h2>
      <div
        v-for="episode in episodesWithCover"
        :key="episode.id"
        class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start gap-4">
          <!-- 剧集封面 -->
          <img
            :src="episode.displayCoverUrl"
            :alt="episode.title"
            class="w-24 h-24 object-cover rounded"
          />

          <!-- 剧集信息 -->
          <div class="flex-1">
            <h3 class="text-xl font-semibold mb-2">{{ episode.title }}</h3>
            <p class="text-gray-600 mb-2 line-clamp-2">{{ episode.description }}</p>
            <div class="flex items-center text-gray-500 text-sm">
              <span>{{ formatDuration(episode.duration) }}</span>
              <span class="mx-2">·</span>
              <span>{{ new Date(episode.published_at).toLocaleDateString() }}</span>
            </div>
          </div>

          <!-- 播放按钮 -->
          <button
            @click="playEpisode(episode)"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full"
          >
            播放
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PodcastAPI } from '@/lib/api'
import type { Podcast, Episode } from '@/lib/types'

const route = useRoute()
const router = useRouter()
const api = new PodcastAPI()

const podcast = ref<Podcast | null>(null)
const episodes = ref<Episode[]>([])
const loading = ref(false)
const error = ref('')

// 为每个剧集添加封面
const episodesWithCover = computed(() => {
  return episodes.value.map(episode => ({
    ...episode,
    displayCoverUrl: episode.cover_url || podcast.value?.cover_url
  }))
})

// 加载播客详情和剧集列表
async function loadPodcastAndEpisodes() {
  loading.value = true
  error.value = ''
  try {
    const podcastId = parseInt(route.params.id as string)
    const [podcastData, episodesData] = await Promise.all([
      api.getPodcast(podcastId),
      api.getEpisodes(podcastId)
    ])
    podcast.value = podcastData
    episodes.value = episodesData
  } catch (e) {
    error.value = '加载数据失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 格式化时长
function formatDuration(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60

  if (hours > 0) {
    return `${hours}小时${remainingMinutes}分钟`
  }
  return `${minutes}分钟`
}

// 播放剧集
function playEpisode(episode: Episode) {
  router.push(`/episode/${episode.id}`)
}

onMounted(loadPodcastAndEpisodes)
</script>
