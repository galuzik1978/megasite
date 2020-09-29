<template>
  <div>
    <v-select 
      v-if="field.type=='select'"
      :prepend-icon=field.icon 
      :placeholder=field.text
      :items=items
      :value="value"
      @input="$emit('input', $event.id)"
      append-outer-icon="mdi-plus"
      @click:append-outer="AddItem"
      item-text="select_name"
      item-value="id"
      return-object
    ></v-select>
    <PopupAdd 
      :dialog=dialog 
      :url=url 
      :content=edit 
      @closeItem="close"
      @select_update="update"></PopupAdd>
  </div>
</template>

<script>
//import PopupAdd from "../components/PopupAdd"

export default {
  name: 'ApiSelect',

  props: {
    field: Object,
    value:{}
  },

  computed:{

    edit: function(){
      return this.$store.state.tables[this.field.subtable].edit
    },

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
    val: ""
  }),

  methods:{

    AddItem: function(){
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
            select_name += " " + element[subname.trim()]
          })

          element['select_name'] = select_name.trim()
          v.items.push(element)
        });
      })
      this.val = this.field.value
    }

  },

  mounted(){
    //Обновляем таблицу при создании компонента
    this.update()
  },

}
</script>

<style>

</style>