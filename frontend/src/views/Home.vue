<template>
  <!-- App.vue -->
  <v-app>
    <v-navigation-drawer 
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
      permanent
      expand-on-hover
    >
      <!-- Главное меню -->
      <v-list dense color="gray">
        <v-list-item-group
          v-model="selectedItem"
          color="primary"
        >
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            link
            @click="change_data(item.table, item.router)"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
           <v-list-item
            :key="100"
            link
            @click="change_data('undefined', '/query')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-file-question-outline</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Заполнить заявку
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            :key="110"
            link
            @click="change_data('undefined', '/inspection')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-wheel-barrow</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Оформить протокол
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <!-- /Главное меню -->
    </v-navigation-drawer>

    <v-app-bar 
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="primary"
      dark
    >
      <!-- -->
      <!-- <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon> -->
      <v-img
        class="mx-2"
        :src="logo"
        max-height="40"
        max-width="40"
        contain
      ></v-img>
      <v-toolbar-title
        style="width: 300px"
        class="ml-0 pl-4"
      >
        <span class="hidden-sm-and-down">{{title}}</span>
      </v-toolbar-title>
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="mdi-magnify"
        label="Search"
        class="hidden-sm-and-down"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-bell</v-icon>
      </v-btn>
      <v-btn icon @click="logout">
        <v-icon>mdi-exit-run</v-icon>
      </v-btn>
    </v-app-bar>
    
    <!-- Sizes your content based upon application components -->
    <v-main>

      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app class="myFont">
      <!-- -->
      <v-spacer></v-spacer>
      <v-banner
        elevation="4"
        icon="mdi-copyright"
        single-line
      >Copyright by ИКЦ Запсиб-Экспертиза</v-banner>
    </v-footer>
  </v-app>
</template>

<script>

  export default {
    components:{
      
    },

    data: () => ({
        drawer: false,
        table_name: '',
        selectedItem: 0
    }),

    computed: {

      title() {
        return this.$store.state.title
      },

      items() {
        return this.$store.state.desktop
      },
      
      loading() {
        return this.$store.state.status == 'loading' ? false : true
      },

      logo(){
        return require("@/assets/" + this.$store.state.logo)
      },

    },

    methods: {

      logout: function() {
        this.$store.dispatch('logout')
        .then(() => {
            this.$router.push('/login')
        })
      },

      change_data: function(data, path){
        if (data!==undefined)
          this.$store.dispatch('change_data', {'name': data.name})
        path = path===undefined ? '/' : path
        if (this.$route.path != path) {
            this.$router.push(path);
        }
      },

    },

    beforeMount() { document.title = this.title },
    beforeUpdate() { document.title = this.title }
}
</script>
<style>
.myFont {
  font-size: 0.8em; 
}
</style>