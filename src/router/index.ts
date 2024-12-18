import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import PodcastList from '../views/PodcastList.vue'
import PodcastDetail from '../components/PodcastDetail.vue'
import EpisodePlayer from '../views/EpisodePlayer.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/podcasts',
    name: 'PodcastList',
    component: PodcastList
  },
  {
    path: '/podcast',
    name: 'PodcastDetail',
    component: PodcastDetail
  },
  {
    path: '/episode/:id',
    name: 'EpisodePlayer',
    component: EpisodePlayer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
