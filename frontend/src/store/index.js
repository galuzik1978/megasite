import Vue from 'vue'
import Vuex from 'vuex'
import axios from '../config-axios'

import { User } from '../api/users'

Vue.use(Vuex)

export default new Vuex.Store({

  state: {
    status:'',
    token: localStorage.getItem('token'),
    company: localStorage.getItem('company'),
    desktop: localStorage.getItem('desktop') === "undefined" ?
      "" : JSON.parse(localStorage.getItem('desktop')),
    logo: localStorage.getItem('logo'),
    role: localStorage.getItem('role'),
    title: localStorage.getItem('title'),
    user: localStorage.getItem('user'),
    tables: localStorage.getItem('tables') === "undefined" ? 
      "" : JSON.parse(localStorage.getItem('tables')),
    current_table: [],
    users: []
  },

  mutations: {

    auth_request(state){
      state.status = 'loading'
    },

    auth_success(state, data){
      state.status = "success"
      state.token = data.token
      state.user = data.user
      state.company = data.company
      state.desktop = data.desktop
      state.logo = data.logo
      state.role = data.role
      state.title = data.title
      state.tables = data.tables
    },

    auth_error(state){
      state.status = 'error'
    },

    logout(state){
      state.status = ''
      state.token = ''
      state.user = {}
      state.template = ''
    },
    
    get_table_data(state){
      state.status = 'request_table_data'
    },

    table_data_recieved(state, {table}){
      state.current_table = table
      state.status = 'table_data_recieved'
    },

    set_users(state, {users}){
      state.users = users
    },

    save_item(state){
      state.status = 'save_item'
    },

    update_item(state){
      state.status = 'update_item'
    },

    action_handler(state){
      state.status = 'action_handler'
    },

    item_saved(state){
      state.status = 'item_saved'
    },

  },
  actions: {

    login({commit}, user){
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({url: '/api-token-auth/', data: user, method: 'POST'})
        .then(resp => {
          const token = resp.data.token
          const user = resp.data.user
          const company = resp.data.company
          const desktop = resp.data.desktop
          const logo = resp.data.logo
          const role = resp.data.role
          const title = resp.data.title
          const tables = resp.data.tables
          localStorage.setItem('token', token)
          localStorage.setItem('user', user)
          localStorage.setItem('company', company)
          localStorage.setItem('desktop', JSON.stringify(desktop))
          localStorage.setItem('logo', logo)
          localStorage.setItem('role', role)
          localStorage.setItem('title', title)
          localStorage.setItem('tables', JSON.stringify(tables))
          commit('auth_success', {
            'user': user,
            'token': token,
            'company': company,
            'desktop': desktop,
            'logo': logo,
            'role': role,
            'title': title,
            'tables': tables
          })
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error')
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },

    logout({commit}){
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('company')
        localStorage.removeItem('desktop')
        localStorage.removeItem('logo')
        localStorage.removeItem('role')
        localStorage.removeItem('title')
        localStorage.removeItem('user')
        localStorage.removeItem('tables')
        delete axios.defaults.headers.common['Authorizaton']
        resolve()
      })
    },

    get_current_table({commit}, url){
      return new Promise((resolve, reject) => {
        commit('get_table_data')
        const token = localStorage.getItem('token')
        axios.defaults.headers.common = {Authorization: 'Token ' + token}
        axios({url: url, method: 'GET'})
        .then(resp => {
          const table = resp.data
          commit('table_data_recieved', table)
          resolve(resp)
        })
        .catch(err => {
          reject(err)
        })
      })
    },

    save_item({commit}, payload){
      return new Promise((resolve, reject) => {
        commit('save_item')
        const token = localStorage.getItem('token')
        axios.defaults.headers.common = {
          Authorization: 'Token ' + token,
          'Content-Type': 'multipart/form-data'
        }
        axios.post(payload.url, payload.data)
        .then(responce => {
          commit('item_saved')
          resolve(responce)
        })
        .catch(err => reject(err))
      })
    },

    update_item({commit}, payload){
      return new Promise((resolve, reject) => {
        commit('update_item')
        const token = localStorage.getItem('token')
        axios.defaults.headers.common = {
          Authorization: 'Token ' + token,
          'Content-Type': 'multipart/form-data'
        }
        axios.put(payload.url + payload.id +"/", payload.data)
        .then(responce => {
          commit('item_saved')
          resolve(responce)
        })
        .catch(err => reject(err))
      })
    },

    action_handler({commit}, payload){
      return new Promise((resolve, reject) => {
        commit('action_handler')
        const token = localStorage.getItem('token')
        axios.defaults.headers.common = {
          Authorization: 'Token ' + token,
          'Content-Type': 'multipart/form-data'
        }
        axios.post(payload.url + payload.id +"/", payload.data)
        .then(responce => {
          commit('item_saved')
          resolve(responce)
        })
        .catch(err => reject(err))
      })
    },

    getUsers({commit}){
      User.list({commit})
      .then(users => {
        commit('set_users', {users})
      })
    }

  },
  modules: {
  },
  getters: {
    isLoggedIn: state => !!state.token,
    table_loading: state => state.status == 'request_table_data' ? true : false,
    users: state => state.users
  }
})
