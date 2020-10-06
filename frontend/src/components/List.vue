<template>
  <div>
    <v-data-table
      :headers="headers"
      :filters="filters"
      :items="table"
      class="elevation-1"
      :calculate-widths=true
      :loading=loading
      loading-text="Загружаем данные ... Пожалуйста, подождите"
      @dblclick:row="editItem"
    >
      <template v-slot:top>
        <v-toolbar flat color="green">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
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
              >{{ new_edit.title }}</v-btn>
            </template>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
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
        <v-btn color="warning" @click="addItem">{{ new_edit.title }}</v-btn>
      </template>
    </v-data-table>
    <popupAdd 
      :dialog=dialog 
      :url=table_url 
      :content=new_edit 
      @closeItem="close"
      @itemsChanged="table_update" 
      :update="update"
      :actions="actions"
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

  props: {
    headers: {},
    filters: {},
    edit: {},
    table_url:{},
    title: {},
    actions: {}
  },

  data:() => ({
    new_edit: {},
    dialog: false,
    table: [],
    update: false
  }),

  computed: {

    loading() {
      return this.$store.getters.table_loading
    }
  },

  methods: {

    addItem(){
      this.new_edit = this.deepClone(this.edit)
      this.update = false
      this.dialog = true
    },

    editItem (event, item) {
      this.new_edit = this.deepClone(this.edit)
      const has = Object.prototype.hasOwnProperty;
      for (var field in item.item){
        if (has.call(this.new_edit.fields, field)){
          this.new_edit.fields[field].value=item.item[field]   
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

    table_update: function (){
      let v = this
      let params = {}
      if(typeof v.filters == "object"){
        v.filters.forEach(filter => {
          params[filter.field] = filter.value
        });
      }
      //Обновляем таблицу при обновлении компонента
      this.$http
      .get(this.table_url, {
          params:params
        }
      )
      .then((response) => {
        v.table = response.data
      })
      v.new_edit = this.deepClone(v.edit)
     },

  },

  watch: {
    table_url: function(new_url){
      let v = this
      //Обновляем таблицу при обновлении компонента
      this.$http
      .get(new_url)
      .then((response) => {
        v.table = response.data
      })
      v.new_edit = this.deepClone(v.edit)
    }
  },

  mounted(){
    this.table_update()
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