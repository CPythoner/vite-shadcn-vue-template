<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 筛选器 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-6">精选英语播客</h1>
      <div class="flex flex-wrap gap-4">
        <select
          v-model="selectedLevel"
          @change="filterPodcasts"
          class="px-4 py-2 border rounded-lg"
        >
          <option value="all">所有级别</option>
          <option value="初级">初级</option>
          <option value="中级">中级</option>
          <option value="高级">高级</option>
        </select>

        <select
          v-model="selectedCategory"
          @change="filterPodcasts"
          class="px-4 py-2 border rounded-lg"
        >
          <option value="all">所有分类</option>
          <option value="听力练习">听力练习</option>
          <option value="口语练习">口语练习</option>
          <option value="新闻">新闻</option>
          <option value="故事">故事</option>
        </select>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-8">
      加载中...
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="text-red-500 text-center py-8">
      {{ error }}
    </div>

    <!-- 播客列表 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="podcast in podcasts"
        :key="podcast.id"
        :to="`/podcast/${podcast.id}`"
        class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow"
      >
        <img
          :src="podcast.cover_url"
          :alt="podcast.title"
          class="w-full h-48 object-cover rounded-t-lg"
        />
        <div class="p-4">
          <h3 class="text-xl font-semibold mb-2">{{ podcast.title }}</h3>
          <div class="flex gap-2 mb-2">
            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
              {{ podcast.level }}
            </span>
            <span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
              {{ podcast.category }}
            </span>
          </div>
          <p class="text-gray-600 mb-2 line-clamp-2">{{ podcast.description }}</p>
          <div class="flex items-center text-gray-500 text-sm">
            <span>{{ podcast.episode_count }}集</span>
            <span class="mx-2">·</span>
            <span>最近更新: {{ new Date(podcast.latest_episode_at).toLocaleDateString() }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { PodcastAPI } from '@/lib/api'
import type { Podcast } from '@/lib/types'

const api = new PodcastAPI()
const podcasts = ref<Podcast[]>([])
const selectedLevel = ref('all')
const selectedCategory = ref('all')
const loading = ref(false)
const error = ref('')

// 加载播客列表
async function loadPodcasts() {
  loading.value = true
  error.value = ''
  try {
    podcasts.value = await api.getAllPodcasts()
  } catch (e) {
    error.value = '加载播客列表失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 筛选播客
async function filterPodcasts() {
  loading.value = true
  error.value = ''
  try {
    if (selectedLevel.value !== 'all') {
      podcasts.value = await api.getPodcastsByLevel(selectedLevel.value)
    } else if (selectedCategory.value !== 'all') {
      podcasts.value = await api.getPodcastsByCategory(selectedCategory.value)
    } else {
      podcasts.value = await api.getAllPodcasts()
    }
  } catch (e) {
    error.value = '筛选播客失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadPodcasts)
</script>
