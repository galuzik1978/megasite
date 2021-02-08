import Vue from 'vue'
import store from '../store/index'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import List from '../components/List.vue'
import Video from '../components/Video.vue'
import Query from '../views/Query.vue'
import Inspection from '../views/Inspection.vue'
import CreateForm from '../views/CreateForm.vue'
import Protocol from '../views/Protocol.vue'
import Contracts from '../views/Contracts.vue'

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
        path:'query/:id',
        name: 'Query',
        component: Query,
        props: true
      },
      {
        path:'inspection',
        name: 'Inspection',
        component: Inspection
      },
      {
        path: 'createform',
        name: 'CreateForm',
        component: CreateForm
      },
      {
        path: 'protocol',
        name: 'Protocol',
        component: Protocol
      },
      {
        path: 'contracts',
        name: 'contracts',
        component: Contracts,
      }
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
