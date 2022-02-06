import Vue from 'vue'
import store from '../store/index'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import List from '../components/List.vue'
import Query from '../views/Query.vue'
import Objects from "../views/Objects.vue"
import Inspection from '../views/Inspection.vue'
import CreateForm from '../views/CreateForm.vue'
import Protocol from '../views/Protocol.vue'
import Contracts from '../views/Contracts.vue'
import NewContract from "../views/NewContract.vue";
import NewQuery from "../views/NewQuery.vue"
import Guest from "../views/Guest.vue"
import Base from '../views/Base.vue'
import SaveQuery from '../views/SaveQuery.vue'
import Administration from '../views/Administration.vue'

Vue.use(VueRouter)

function dynamicPropsFn (route) {
  return {
    wr_id: parseInt(route.params.wr),
    obj_id: parseInt(route.params.id)
  }
}

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
        props: true,
      },
      {
        path:'query/:id',
        name: 'Query',
        component: Query,
        props: true,
        
      },
      {
        path: 'objects',
        name: 'Objects',
        component: Objects,
        props: true,
      },
      {
        path:'inspection',
        name: 'Inspection',
        component: Inspection,
      },
      {
        path: 'createform',
        name: 'CreateForm',
        component: CreateForm,
      },
      {
        path: 'newcontract',
        name: 'NewContract',
        component: NewContract,
      },
      {
        path: 'protocol/:id',
        name: 'Protocol',
        component: Protocol,
        props: dynamicPropsFn,
      },
      {
        path: 'contracts',
        name: 'contracts',
        component: Contracts,
      },
      {
        path: 'administration',
        name: 'administration',
        component: Administration,
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/guest',
    component: Guest,
    children:[
      {
        path: '/',
        name: 'BasePage',
        component: Base
      },
      {
        path: 'start',
        name: 'AnonimeNewQuery',
        component: NewQuery,
      },
      {
        path: 'login',
        name: 'Anonimelogin',
        component: Login
      },
      {
        path: 'savequery',
        name: 'SaveQuery',
        component: SaveQuery,
        props: true,
      },
    ]
  },
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
    next({
      path: '/guest',
    })
  } else {
    next()
  }
})

export default router
