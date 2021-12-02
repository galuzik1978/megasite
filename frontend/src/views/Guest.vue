<template>
  <v-app id="inspire">
    
    <v-app-bar app
      color="primary"
      dark
    >
      <v-img
        class="mx-2"
        :src="logo"
        max-height="40"
        max-width="40"
        contain
      ></v-img>
      <v-toolbar-title>ИКЦ Запсиб-Экспертиза</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="login">
        <v-icon>mdi-login</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  export default {
    data: () => ({ drawer: null }),

    computed:{
      logo(){
        return require("@/assets/Penrose-dreieck.svg")
      },
    },

    methods:{
      login(){
        this.$router.push('/guest/login')
      }
    }
  }
</script>