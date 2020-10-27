import Vue from 'vue'
import store from '../store/index'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import List from '../components/List.vue'
import Video from '../components/Video.vue'
import Query from '../views/Query.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    component: Home,
    meta: {
      requiredAuth: true
    },
    children: [
      {
        path: '',
        name: 'Table',
        component: List,
        props: true
      },
      {
        path:'video',
        name: 'Video',
        component: Video
      },
      {
        path:'query',
        name: 'Query',
        component: Query
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  }
]

const router = new VueRouter({
  //mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiredAuth)) {
    if (store.getters.isLoggedIn == true){
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
