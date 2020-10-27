<template>
  <div>
    <v-data-table
      :items="items"
      :headers="table.headers"
      class="elevation-1"
      :calculate-widths=true
      :loading=loading
      loading-text="Загружаем данные ... Пожалуйста, подождите"
      @dblclick:row="editItem"
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
    <popupAdd 
      :dialog=dialog 
      :table=table 
      :content=content 
      @closeItem="close"
      @itemsChanged="table_update"
      :update="update"
    >
    </popupAdd>
  </div>
</template>

<script>
import popupAdd from '../components/PopupAdd'
export default {

  components:{
    popupAdd
  },

  data:() => ({
    content:{},
    dialog: false,
    update: false,
    items:[]
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

  },

  methods: {

    addItem(){
      this.content = this.deepClone(this.table.edit)
      this.update = false
      this.dialog = true
    },

    editItem (event, item) {
      this.content = this.deepClone(this.table.edit)
      var tmp
      if (item.item == undefined) {
        tmp = item
      } else {
        tmp = item.item
      }
      
      const has = Object.prototype.hasOwnProperty;
      for (var field in tmp){
        if (has.call(this.content.fields, field)){
          this.content.fields[field].value=tmp[field]   
        }
      }
      this.update = true
      this.dialog = true
    },

    close () {
      this.dialog = false
    },

    deepClone: function (obj) {
      const clObj = {};
      for(const i in obj) {
        if (obj[i] instanceof Object) {
          clObj[i] = this.deepClone(obj[i]);
          continue;
        }
        clObj[i] = obj[i];
      }
      return clObj;
    },

    table_update(table, content) {
      let params = {}
      if(typeof this.table.filters == "object")
        this.table.filters.forEach(filter => {
          params[filter.field] = filter.value
        });
      if (typeof content == "undefined") {
        //Обновляем таблицу при обновлении компонента
        this.$http
        .get(this.table_url, {
            params:params
          }
        )
        .then((response) => {
          this.items = response.data
        })
        this.content = this.deepClone(this.table.edit)
      } else {
        this.$store.dispatch('change_data', {'name': table.name})
        this.content = this.deepClone(content)
        this.dialog = true 
      }
    },

  },

  watch: {
    table_name: {
      immediate: true,
      handler(){
        //Обновляем таблицу при обновлении компонента
        let params = {}
        if(typeof this.table.filters == "object")
          this.table.filters.forEach(filter => {
            params[filter.field] = filter.value
          });
        this.$http
        .get(this.table_url, {
          params:params
        })
        .then((response) => {
          this.items = response.data
        })
        this.popup_key = this.table_url
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

</style>