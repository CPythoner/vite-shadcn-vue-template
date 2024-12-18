<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 筛选器 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-6">精选英语播客</h1>
      <div class="flex flex-wrap gap-4">
        <select
          v-model="selectedLevel"
          class="px-4 py-2 border rounded-lg"
        >
          <option value="all">所有级别</option>
          <option value="初级">初级</option>
          <option value="中级">中级</option>
          <option value="高级">高级</option>
        </select>

        <select
          v-model="selectedCategory"
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

    <!-- 播客列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="podcast in filteredPodcasts"
        :key="podcast.id"
        :to="podcast.link"
        class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow"
      >
        <img
          :src="podcast.cover"
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
          <p class="text-gray-600 mb-2">{{ podcast.description }}</p>
          <div class="flex items-center text-gray-500 text-sm">
            <span>更新至: {{ podcast.latestUpdate }}</span>
            <span class="mx-2">·</span>
            <span>{{ podcast.episodeCount }}集</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const selectedLevel = ref('all')
const selectedCategory = ref('all')

const podcasts = ref([
  {
    id: 1,
    title: "Listening Time: English Practice",
    description: "这个播客专门为想要练习听力的英语学习者设计。美国人用自然的语速讲述不同的话题，帮助你提升听力理解能力。",
    level: "初级",
    category: "听力练习",
    cover: "https://megaphone.imgix.net/podcasts/8a82f080-b6d1-11ed-a66a-23530cf4974e/image/8bfa793d0e9e45ba9ce5f6bd3464523e.jpg",
    link: "/podcast",
    latestUpdate: "2024-03-14",
    episodeCount: 156
  },
  {
    id: 2,
    title: "IELTS Speaking for Success",
    description: "雅思口语考试备考必听播客，每期讲解不同的口语话题和答题技巧，帮助你提高口语分数。",
    level: "中级",
    category: "口语练习",
    cover: "https://example.com/ielts-speaking.jpg",
    link: "/podcast/ielts-speaking",
    latestUpdate: "2024-03-13",
    episodeCount: 89
  },
  {
    id: 3,
    title: "Easy Stories in English",
    description: "通过简单的英语故事提升听力理解能力，适合初学者。每个故事都经过精心改编，配有详细的生词解释。",
    level: "初级",
    category: "故事",
    cover: "https://example.com/easy-stories.jpg",
    link: "/podcast/easy-stories",
    latestUpdate: "2024-03-12",
    episodeCount: 245
  },
  {
    id: 4,
    title: "The A to Z English Podcast",
    description: "从A到Z系统地学习英语，涵盖语法、词汇、发音等各个方面。每集都有实用的英语表达和练习。",
    level: "中级",
    category: "听力练习",
    cover: "https://example.com/atoz.jpg",
    link: "/podcast/atoz",
    latestUpdate: "2024-03-11",
    episodeCount: 178
  },
  {
    id: 5,
    title: "6 Minute English",
    description: "BBC出品的六分钟英语节目，每期讨论一个有趣的话题，配有词汇解释和练习。",
    level: "中级",
    category: "新闻",
    cover: "https://example.com/6min.jpg",
    link: "/podcast/6min",
    latestUpdate: "2024-03-10",
    episodeCount: 523
  }
])

const filteredPodcasts = computed(() => {
  return podcasts.value.filter(podcast => {
    if (selectedLevel.value !== 'all' && podcast.level !== selectedLevel.value) return false
    if (selectedCategory.value !== 'all' && podcast.category !== selectedCategory.value) return false
    return true
  })
})
</script>
