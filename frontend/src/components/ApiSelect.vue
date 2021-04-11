<template>
  <div>
    <v-select 
      :prepend-icon=field.icon 
      :placeholder=field.text
      :items=items
      :value="val"
      @input="$emit('input', $event)"
      item-text="select_name"
      item-value="id"
      return-object
    >
    <template v-slot:append-outer>
      <v-icon v-if="value" @click="EditItem(value)">
        mdi-pencil
      </v-icon>
      <v-icon @click="AddItem">
        mdi-plus
      </v-icon>
    </template>
    </v-select>
    <PopupAdd 
      :dialog=dialog 
      :table=table  
      :content=edit 
      @closeItem="close"
      @select_update="update"
      @itemsChanged="update"
    ></PopupAdd>
  </div>
</template>

<script>
//import PopupAdd from "../components/PopupAdd"

export default {
  name: 'ApiSelect',

  props: {
    field: Object,
    value:{},
    table:{}
  },

  computed:{

    url: function(){
      return this.$store.state.tables[this.field.subtable].url
    },

  },

  components:{
    PopupAdd: () => import('../components/PopupAdd')
  },

  data: () => ({
    fields: [],
    dialog: false,
    items: [],
    val: "",
    edit:{}
  }),

  methods:{

    AddItem: function(){
      this.dialog = true
    },

    EditItem (item) {
      this.edit = this.table.edit
      if (typeof item == "number"){
        this.edit.fields.id.value = item
      } else {
        const has = Object.prototype.hasOwnProperty;
        for (var field in item){
          if (has.call(this.edit.fields, field)){
            this.edit.fields[field].value=item[field]   
          } else if (typeof item[field] === "object") {
            for (var sub_field in item[field]){
              if (has.call(this.edit.fields, `${field}.${sub_field}`)){
                this.edit.fields[`${field}.${sub_field}`].value=item[field][sub_field]   
              }
            }
          } 
        }
      }
      this.update = true
      this.dialog = true
    },

    close () {
      this.dialog = false
    },

    update(){
      let v = this
      //Обновляем таблицу при создании компонента
      this.$http
      .get(this.url)
      .then((response) => {
        response.data.forEach(element => {
          let n = v.field.name.split("+")
          let select_name = ""
          n.forEach(subname => {
            let val = element
            let f = subname.trim().split(".")
            f.forEach(subfield => {
              val = val[subfield]
            })
            select_name += " " + val
          })

          element['select_name'] = select_name.trim()
          v.items.push(element)
        });
        v.val = v.field.value
      })
    }

  },

  created(){
    //Обновляем таблицу при создании компонента
    this.edit=this.$store.state.tables[this.field.subtable].edit
    this.update()
  },

}
</script>

<style>

</style>