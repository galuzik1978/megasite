<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',

  data: () => ({
    //
  }),
  computed: {
    isLoggedIn: function(){
      return this.$store.getters.isLoggedIn
    }
  },
  created: function() {
    this.$http.interceptors.response.use(undefined, function(err){
      return new Promise(function (){
        if(err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err;
      });
    });
  }
}
</script>

<style>

</style>