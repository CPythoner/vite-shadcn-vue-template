import type { RouteRecordRaw } from 'vue-router'

const podcastRoutes: RouteRecordRaw[] = [
  {
    path: '/podcasts',
    name: 'podcasts',
    component: () => import('@/views/PodcastList.vue'),
    meta: {
      title: '播客列表'
    }
  },
  {
    path: '/podcast/:id',
    name: 'podcast-detail',
    component: () => import('@/views/PodcastDetail.vue'),
    meta: {
      title: '播客详情'
    }
  },
  {
    path: '/episode/:id',
    name: 'episode-player',
    component: () => import('@/views/EpisodePlayer.vue'),
    meta: {
      title: '剧集播放'
    }
  }
]

export default podcastRoutes
