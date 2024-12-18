<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-20">
      <div class="container mx-auto px-4">
        <h1 class="text-5xl font-bold mb-6">
          通过播客学习语言，让学习更有趣
        </h1>
        <p class="text-xl mb-8">
          精选全球优质播客内容，配合智能学习工具，帮助你快速提升语言能力
        </p>
        <router-link
          to="/podcasts"
          class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-opacity-90"
        >
          开始学习
        </router-link>
      </div>
    </div>

    <!-- Features Section -->
    <div class="container mx-auto px-4 py-16">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-semibold mb-4">分级学习内容</h3>
          <p class="text-gray-600">
            从初级到高级的内容分级，帮助你循序渐进提升语言能力
          </p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-semibold mb-4">智能学习工具</h3>
          <p class="text-gray-600">
            实时字幕、速度调节、生词本等功能，让学习更高效
          </p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-semibold mb-4">社区互动</h3>
          <p class="text-gray-600">
            加入学习小组，与其他学习者交流分享，互相进步
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>
