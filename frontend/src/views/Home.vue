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
          <v-list-item
            :key="120"
            link
            @click="change_data('undefined', '/createform')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-creation</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Создать новую форму протокола
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            :key="130"
            link
            @click="change_data('undefined', '/protocol/5/')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-creation</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Заполнить протокол
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            :key="150"
            link
            @click="change_data('undefined', '/administration')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-database-edit</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Сформировать меню для ролей
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            :key="200"
            link
            @click="change_data(items[2].table, '/queries')"
            active-class="active-menu-btn"
          >
            <v-list-item-action style="width:24px">
              <v-icon>mdi-database-search</v-icon>
            </v-list-item-action>
            <v-list-item-content class="text-left">
              <v-list-item-title>
                Работа с заявками
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <!-- /Главное меню -->
    </v-navigation-drawer>

    <!-- Верхняя панель сайта -->
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
      <!-- If using vue-router -->
      <router-view></router-view>
    </v-main>

    <v-footer 
      padless 
      app 
    >
      <v-card class="text-right black--text" width="100%">
        <!-- -->
        <v-spacer></v-spacer>
        <v-card-text>
          <v-icon color="black">mdi-copyright</v-icon> Copyright by ИКЦ Запсиб-Экспертиза
        </v-card-text>
      </v-card>
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
        selectedItem: 3
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

    mounted(){
      this.selectedItem = this.$store.state.start_page
    },

    beforeMount() { document.title = this.title },
    beforeUpdate() { document.title = this.title }
}
</script>
<style>
.myFont {
  font-size: 0.6em; 
}

</style>