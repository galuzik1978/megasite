<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
    >
      <!-- Главное меню -->
      <v-list dense color="gray">
        <template v-for="item in items">
          <v-list-item
            :key="item.text"
            link
            @click="change_data(item.table)"
            :to="item.router===undefined ? '/' : item.router"
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
        </template>
      </v-list>
      <!-- /Главное меню -->
    </v-navigation-drawer>

    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="green darken-3"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
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
    <v-main>
      <v-container fluid fill-height>
        <v-layout child-flex>
          <router-view
            :table=table
            @ListChanged=change_table
          ></router-view>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
    props: {
      items: Array
    },

    data: () => ({
        drawer: false,
        table_name: '',
    }),

    computed: {

      title: function(){
        return this.$store.state.company
      },

      logo(){
        return require("@/assets/" + this.$store.state.logo)
      },

      table() {
        return this.$store.state.tables[this.table_name]
      }

    },
    methods: {

      logout: function() {
        this.$store.dispatch('logout')
        .then(() => {
            this.$router.push('/login')
        })
      },

      change_data: function(data){
        if (data!==undefined)
          this.table_name = data.name
      },
      
      change_table(table){
        this.table_name = table.name
      }

    },
    
    created: function(){
      this.table_name = this.$store.state.desktop[0].table.name
    }
}
</script>
<style scoped>
.active-menu-btn{
  opacity: 70%;
}
</style>