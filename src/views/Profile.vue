<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 用户信息 -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="flex items-center gap-6">
        <img
          src="https://placeholder.com/100"
          alt="用户头像"
          class="w-24 h-24 rounded-full"
        />
        <div>
          <h2 class="text-2xl font-bold mb-2">张三</h2>
          <p class="text-gray-600">学习英语 · 当前等级：中级</p>
        </div>
      </div>
    </div>

    <!-- 学习统计 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold mb-2">学习时长</h3>
        <p class="text-3xl font-bold text-blue-600">24.5</p>
        <p class="text-gray-600">小时</p>
      </div>
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold mb-2">已学播客</h3>
        <p class="text-3xl font-bold text-blue-600">15</p>
        <p class="text-gray-600">个</p>
      </div>
      <div class="bg-white rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold mb-2">掌握单词</h3>
        <p class="text-3xl font-bold text-blue-600">230</p>
        <p class="text-gray-600">个</p>
      </div>
    </div>

    <!-- 最近学习 -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h3 class="text-xl font-semibold mb-4">最近学习</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded">
          <div>
            <h4 class="font-medium">英语新闻早餐 #123</h4>
            <p class="text-gray-600">上次学习：2024-03-10</p>
          </div>
          <div class="text-right">
            <p class="text-blue-600">进度：75%</p>
            <button class="text-blue-600">继续学习</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的生词本 -->
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h3 class="text-xl font-semibold mb-4">我的生词本</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded">
          <div>
            <span class="font-medium">vocabulary</span>
            <span class="text-gray-500 ml-2">[vəˈkæbjələri]</span>
            <p class="text-gray-600">词汇、词表</p>
          </div>
          <button class="text-red-600">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 组件逻辑
</script>
