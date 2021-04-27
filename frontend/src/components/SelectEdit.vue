<template>
<div :key=key>
  <v-select 
    :items='items'
    v-model="row[index]"
    item-text="val"
    item-value="id"
  >
    <template v-slot:append-outer>
      <v-icon @click="dialog=true">
        mdi-pencil-plus-outline
      </v-icon>
    </template>
  </v-select>
  <v-dialog
    v-model="dialog"
    width="500"
    
  >          
    <v-card>
      <v-card-title class="headline grey lighten-2">
        Выбираемые параметры
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-for="(col, index) in items"
          :key="index"
          v-model="items[index]"
        ></v-text-field>
        <v-btn 
          icon 
          elevation="2"
          @click="add_select(items)"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="dialog = false"
        >
          Закрыть
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script>
export default {
  
  data:() => ({
    dialog:false,
    key:0
  }),

  props:{
    items: Array,
    row: Object,
    index: String,
    item_text: String
  },

  methods:{
    add_select(items){
      this.items.splice(items.length,0,"")
      this.key+=1
    }
  },

}
</script>

<style>

</style>