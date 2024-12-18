<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <!-- 播客头部信息 -->
      <div class="flex flex-col md:flex-row gap-8 mb-8">
        <img
          src="https://megaphone.imgix.net/podcasts/8a82f080-b6d1-11ed-a66a-23530cf4974e/image/8bfa793d0e9e45ba9ce5f6bd3464523e.jpg"
          alt="Podcast Cover"
          class="w-48 h-48 rounded-lg object-cover"
        />
        <div>
          <h1 class="text-3xl font-bold mb-2">Listening Time: English Practice</h1>
          <p class="text-gray-600 mb-4">By Sonoro | Conner Pe</p>
          <p class="text-gray-700">
            This podcast is for English learners who want to practice their listening comprehension in a natural way.
            In each episode, an American speaker talks about different topics without reading a script.
            He speaks in a natural way, with native words and phrases, but he speaks a little more slowly
            and clearly than other native speakers.
          </p>
        </div>
      </div>

      <!-- 最新剧集列表 -->
      <div>
        <h2 class="text-2xl font-bold mb-4">Latest Episodes</h2>
        <div class="space-y-4">
          <router-link
            v-for="episode in latestEpisodes"
            :key="episode.id"
            :to="`/episode/${episode.id}`"
            class="block border rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer"
          >
            <h3 class="text-xl font-semibold mb-2">{{ episode.title }}</h3>
            <p class="text-gray-600 mb-2">{{ episode.date }}</p>
            <p class="text-gray-700">{{ episode.description }}</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const latestEpisodes = [
  {
    id: '1',
    title: "English Listening - Techniques For Learning Vocabulary",
    date: "December 16, 2024",
    description: "Practice your English listening as I talk about some techniques for learning vocabulary.",
    audioUrl: "https://dts.podtrac.com/redirect.mp3/chrt.fm/track/G8F1AF/traffic.megaphone.fm/SONORO7201496122.mp3",
    transcriptUrl: "https://drive.google.com/file/d/1b8lSjpKxbcRWJS-JOJAoK0DKm4Y97UZI/view"
  },
  {
    id: '2',
    title: "English Phrasal Verbs - Bank On, Bargain For",
    date: "December 13, 2024",
    description: "Learn the phrasal verbs 'bank on' and 'bargain for' naturally, through listening.",
    audioUrl: "https://example.com/audio2.mp3"
  },
  {
    id: '3',
    title: "English Listening - Reality TV",
    date: "December 9, 2024",
    description: "Practice your English listening as I talk about reality TV.",
    audioUrl: "https://example.com/audio3.mp3"
  }
]
</script>
