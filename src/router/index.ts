import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import PodcastList from '../views/PodcastList.vue'
import PodcastDetail from '../views/PodcastDetail.vue'
import EpisodePlayer from '../views/EpisodePlayer.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/podcasts',
    name: 'podcasts',
    component: PodcastList,
    meta: {
      title: '播客列表'
    }
  },
  {
    path: '/podcast/:id',
    name: 'podcast-detail',
    component: PodcastDetail,
    meta: {
      title: '播客详情'
    }
  },
  {
    path: '/episode/:id',
    name: 'episode-player',
    component: EpisodePlayer,
    meta: {
      title: '剧集播放'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
