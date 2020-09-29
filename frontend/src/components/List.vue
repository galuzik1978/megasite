<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="table"
      sort-by="calories"
      class="elevation-1"
      :calculate-widths=true
      :loading=loading
      loading-text="Загружаем данные ... Пожалуйста подождите"
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
                v-on="on"
              >Экспорт</v-btn>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >{{ edit.title }}</v-btn>
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
      <template v-slot:item.annex="{ item }">
        {{ item.annex | limitStr }}
      </template>
      <template v-slot:no-data>
        <v-btn color="warning" @click="addItem">{{ edit.title }}</v-btn>
      </template>
    </v-data-table>
    <popupAdd :dialog=dialog :url=table_url :content=new_edit @closeItem="close"></popupAdd>
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
    edit: {},
    table_url:{},
    title: {}
  },

  data:() => ({
    new_edit: {},
    dialog: false,
    table: []
  }),

  computed: {

    loading() {
      return this.$store.getters.table_loading
    }
  },

  methods: {

    addItem(){
      this.new_edit = this.edit
      this.dialog = true
    },

    editItem (event, item) {
      let new_edit = this.edit
      const has = Object.prototype.hasOwnProperty;
      for (var field in item.item){
        if (has.call(new_edit.fields, field)){
          if ((typeof(item.item[field]) == "object")&&(item.item[field] !== null)){
            let f = new_edit.fields[field].name.split("+")
            let value = ""
            f.forEach(element => {
              value += " " + item.item[field][element.split('.')[1]]
            });
            new_edit.fields[field].value = value.trim()
          } else {
            new_edit.fields[field].value=item.item[field]
          }        
        }
          
      }
      this.new_edit = this.edit
      this.dialog = true
    },

    close () {
      this.dialog = false
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
      v.new_edit = v.edit
    }
  },

  mounted(){
    let v = this
    //Обновляем таблицу при создании компонента
    this.$http
    .get(this.table_url)
    .then((response) => {
      v.table = response.data
    })
    v.new_edit = v.edit
  },

  filters: {
    limitStr: function (value, n=50) {
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