<template>
  <v-data-table
      :items="items"
      :headers="table.headers"
      class="elevation-1"
      :calculate-widths=true
      :loading=loading
      loading-text="Загружаем данные ... Пожалуйста, подождите"
      no-data-text="Записи таблицы не найдены."
      @click:row="editItem"
    >
      <template v-slot:top>
        <v-toolbar flat color="success">
          <v-toolbar-title>{{ table.title }}</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="secondary"
                dark
                class="mb-2"
                v-bind="attrs"
                @click="addItem"
              >Экспорт</v-btn>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                @click="addItem"
              >{{ table.edit.title }}</v-btn>
            </template>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem ($event, item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:item.link="{ item }">
        <a :href="item.annex" target="_blank">{{ item.annex | limitStr }}</a>
      </template>
      <template v-slot:no-data>
        <v-btn color="warning" @click="addItem">{{ table.edit.title }}</v-btn>
      </template>
    </v-data-table>
</template>

<script>
  export default {
    props:{
      id: Number,
    },

    data:() => ({
      content:{},
      dialog: false,
      update: false,
    }),

    computed: {

      loading() {
        return this.$store.getters.table_loading
      },

      table_name() {
        return this.$store.state.table_name
      },

      table_url(){
        return this.$store.state.tables[this.table_name].url
      },

      table(){
        return this.$store.state.tables[this.table_name]
      },

      items(){
        return this.$store.state.current_table
      },

    },

    methods:{
      
      addItem(event, item){
        console.log(event, item)
        this.$router.push({name: 'NewQuery',  params: {id:null}, query:{id: null}});
      },

      editItem(event, item){
        console.log(event, item)
        this.$router.push({name: 'NewQuery',  params: {id:event.id}, query:{id: event.id}});
      },

      table_update() {
        let params = {}
          if(typeof this.table.filters == "object")
            this.table.filters.forEach(filter => {
              params[filter.field] = filter.value
            });
          this.$store.dispatch('get_current_table', {'url': this.table_url, 'params': params})
          this.popup_key = this.table_url
          this.dialog = false
      },
    },

    watch: {
      table_name: {
        immediate: true,
        handler(){
          //Обновляем таблицу при обновлении компонента
          this.table_update()
        }
      }
    },

    filters: {
      limitStr: function (value, n=20) {
        if (value){
          if (value.length < n) return value;
          let symb = '...';
          return value.substr(0, n - symb.length) + symb;
        }
        return value
      }
    }
  }
</script>

<style>
  .container.fill-height{
    margin: 0;
    padding: 0;
    align-items: stretch;
  }
  .half-height{
    height: 50%;
    padding: 0;
    background-color: pink;
  }

  .grid-item-blue {
    background-color: lightblue;
    align-items: stretch;
  }

  .grid-item-green {
    background-color: lightgreen;
    overflow-y: scroll;
  }

  .grid-item-pink {
    background-color: pink;

  }
  .grid-item-green>p{
      height:9000px;
      border:10px solid;
      margin:20px;
  }

  .fill-parent-height {
    height: 50vh;
  }

  .top-row{
      max-height: 100%;
  }

</style>