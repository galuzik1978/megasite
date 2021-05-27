<template>
  <table class="grid_table">
    <thead>
      <tr>
        <th
          v-for="(header, i) in headers"
          :key='i'
        >{{ header.text }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, i) in items" :key="i">
        <td v-for="(sell, index) in headers" :key="index"
        >
          <template v-if='sell.type=="rows_num"'>
            {{ i+1 }}
          </template>
          <template
            v-else-if='sell.type=="sorting"'
          >
            <v-btn small @click="$emit('up', i)"><v-icon>mdi-arrow-up-drop-circle</v-icon></v-btn>
            <v-btn small @click="$emit('down', i)"><v-icon>mdi-arrow-down-drop-circle</v-icon></v-btn>
          </template>
          <template v-else-if='sell.editable^creating'>
            <template v-if='sell.type=="select"'>
              <select_edit
                :items="'select_items' in sell ? sell.select_items : (sell = Object.assign({}, sell, { select_items: [] }))['select_items']"
                :row="row"
                :index="sell.value"
              ></select_edit>
            </template>
            <v-checkbox
              v-else-if='sell.type=="bool"'
              v-model="row[sell.value]"
            ></v-checkbox>
            <v-text-field 
              v-else-if='sell.type=="number"'
              v-model="row[sell.value]"
              type="number"
              :min="'range' in sell ? sell.range[0] : null"
              :max="'range' in sell ? sell.range[1] : null"
              :step="'range' in sell ? sell.range[2] : null"
            ></v-text-field>
            <v-text-field v-else
              v-model="row[sell.value]"
            ></v-text-field>
          </template>
          <template v-else>
            {{ row[sell.value] }}
          </template>
        </td>
      </tr>
    </tbody>
</table>
</template>

<script>
import select_edit from '../components/SelectEdit'

export default {

  components:{
    select_edit
  },

  data:() => ({
    dialog:false
  }),

  props:{
    headers:Array,
    items:Array,
    item_text: String,
    creating:{
      type: Boolean,
      default: false
    }
  },
}
</script>

<style scoped>
  div >>> .grid_table{
    width: 100%;
  }
</style>