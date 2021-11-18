<template>
  <v-card flat>
    <v-alert
      :value="alert"
      color="pink"
      dark
      border="top"
      icon="mdi-home"
      transition="scale-transition"
    >
      Phasellus tempus. Fusce ac felis sit amet ligula pharetra condimentum. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. Pellentesque posuere. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo.

      Phasellus nec sem in justo pellentesque facilisis. Phasellus magna. Cras risus ipsum, faucibus ut, ullamcorper id, varius ac, leo. In hac habitasse platea dictumst. Praesent turpis.
    </v-alert>
    <v-card-title class="text-center justify-center">
      Выберите существующую таблицу
    </v-card-title>
    <v-card-text>
      <v-list dense>
        <v-subheader>Формы таблиц</v-subheader>
        <v-list-item-group
          v-model="selectedTable"
          color="primary"
          mandatory
        >
          <v-list-item
            @click="fill_table(-1)"
          >
            <v-list-item-icon>
              <v-icon>mdi-table-large-plus</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Новая таблица</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-for="(item, i) in tables"
            :key="i"
            @click="fill_table(i)"
          >
            <v-list-item-icon>
              <v-icon>mdi-form-dropdown</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          
        </v-list-item-group>
      </v-list>
    </v-card-text>
    <v-card-title class="text-center justify-center">
      Сформируйте все столбцы и строки таблицы контроля
    </v-card-title>
    <v-row justify='center'>
      <v-col
        cols=6
      >
        <v-text-field
          label="Введите наименование таблицы"
          v-model="data.tables[0].name"
        >
        </v-text-field>
      </v-col>
    </v-row>
    <v-card-subtitle>
      Заголовок таблицы
    </v-card-subtitle>
    <v-card-text>
      <custom_table
        :headers="table_headers"
        :items="data.tables[0].header"
        @up="sorting_up($event)"
        @down="sorting_down($event)"
        @delete="sorting_delete($event)"
      >
      </custom_table>
      <v-btn color="warning" @click="addCol({headers:table_headers, items:data.tables[0].header})">Добавить столбец таблицы</v-btn>
    </v-card-text>
    <v-card-subtitle>
      Содержимое таблицы
    </v-card-subtitle>
    <v-card-text>
      <custom_table
        :headers="data.tables[0].header.concat([{text: 'sorting', type: 'sorting'}])"
        :items="data.tables[0].dataset"
        :creating=true
        @up="sorting_up($event)"
        @down="sorting_down($event)"
        @delete="sorting_delete($event)"
      >
      </custom_table>
      <v-btn color="warning" @click="addRow({headers:table_items, items:data.tables[0].data_set})">Добавить строку таблицы</v-btn>
    </v-card-text>
    <v-card-subtitle>
      Данные для выпадающих списков
    </v-card-subtitle>
    <div
      v-for="(col, index) in data.tables[0].header"
      :key='"select" + index'
    >
      <div
        v-if="col.type=='3'"
      >
        <v-card-subtitle>
          {{ col.text }}
        </v-card-subtitle>
        <custom_table
          :headers="select_header"
          :items="col.selectchoices"
          :creating=true
          
        >
        </custom_table>
        <v-btn color="warning" @click="addSelect({headers:select_header, items:col.selectchoices}); data=data">Добавить строку таблицы</v-btn>
      </div>
    </div>
    <v-card>
      <v-card-subtitle>Пример отображения таблицы в протоколе</v-card-subtitle>
      <protocolTable
        :tables=data.tables
        :annex_table=data.annex_table
        :images=images
        :data=data
        :key=selectedTable
      ></protocolTable>
    </v-card>
    <v-btn block color="error" @click="saveTable">Сохранить все изменения в таблице</v-btn>
  </v-card>
</template>

<script>
import protocolTable from '../components/ProtocolTable'
import custom_table from '../components/CustomTable'

export default {
  components:{
    protocolTable,
    custom_table,
  },

  data:() => ({
    alert: false,

    table_headers:[
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%',
        type: 'rows_num',
      },
      {
        text: 'text',
        align: 'start',
        sortable: false,
        value: 'text',
        editable: true
      },
      {
        text: 'value',
        align: 'start',
        sortable: false,
        value: 'value',
        editable: true,
      },
      {
        text: 'data',
        align: 'start',
        sortable: false,
        value: 'data',
        editable: true
      },
      {
        text: 'sortable',
        align: 'start',
        sortable: false,
        value: 'sortable',
        type: 'bool',
        editable: true
      },
      {
        text: 'editable',
        align: 'start',
        sortable: false,
        value: 'editable',
        type: 'bool',
        editable: true
      },
      {
        text: 'align',
        align: 'start',
        sortable: false,
        value: 'align',
        type: 'select',
        select_items:[
          {
            id:'1',
            val:'none'
          },
          {
            id:'2',
            val:'start'},
          {
            id:'3',
            val:'center'},
          {
            id:'4',
            val:'end'
          }
        ],
        editable: true
      },
      {
        text: 'width',
        align: 'start',
        sortable: false,
        value: 'width',
        editable: true,
        type: 'number',
        range: [0,100,3]
      },
      {
        text: 'type',
        align: 'start',
        sortable: false,
        value: 'type',
        type: 'select',
        select_items:[
          {
            id:'1',
            val:'none'
          },
          {
            id:'2',
            val:'bool'
          },
          {
            id:'3',
            val:'select'
          },
          {
            id:'4',
            val:'actions'
          },
          {
            id:'5',
            val:'rows_num'
          },
        ],
        editable: true
      },
      {
        text: 'action',
        align: 'start',
        sortable: false,
        value: 'width',
        type: 'select',
        select_items:[
          {
            id:'1',
            val:'none'
          },
          {
            id:'2',
            val:'del'
          },
          {
            id:'3',
            val:'add'
          },
        ],
        editable: true
      },
      {
        text: 'sorting',
        type: 'sorting'
      }
    ],

    images:[],

    table_items:[],

    selectedTable:-1,

    select_header:[
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%',
        type: 'rows_num',
      },
      {
        text: 'Значение',
        align: 'start',
        sortable: false,
        value: 'value',
        editable: true
      },
      {
        text: 'Текст',
        align: 'start',
        sortable: false,
        value: 'text',
        editable: true
      },
    ]

  }),

  props:{
    data:Object,
    tables:Array
  },

  methods:{
    
    addCol(table){
      let row = {}
      for (let item of table.headers){
        row[item.value] = null
      }
      row.selectchoices = []
      table.items.push(
        row
      )
    },

    addRow(table){
      let row = {annex_table:[]}
      for (let item of table.headers){
        row[item.value] = null
      }
      row.selectchoices = []
      table.items.push(
        row
      )
    },
    
    addSelect(table){
      let row = []
      for (let item of table.headers){
        row[item.value] = null
      }
      row.selectchoices = []
      table.items.push(
        row
      )
    },

    sorting_up(event){
      if (event.i > 0){
        [event.items[event.i-1], event.items[event.i]] = [event.items[event.i], event.items[event.i-1]];
        [event.items[event.i-1].order, event.items[event.i].order] = [event.items[event.i].order, event.items[event.i-1].order]
        console.log('up')
        console.log(event)
        event.items.splice()
      }
    },

    sorting_down(event){
      if (event.i < (event.items.length - 1)){
        [event.items[event.i+1], event.items[event.i]] = [event.items[event.i], event.items[event.i+1]];
        [event.items[event.i+1].order, event.items[event.i].order] = [event.items[event.i].order, event.items[event.i+1].order]
        console.log('down')
        console.log(event)
        event.items.splice()
      }
    },

    sorting_delete(event){
      console.log('delete')
      console.log(event)
      event.items.splice(event.i, 1)
    },

    fill_table(event){
      if (event >= 0){
        this.data.tables[0] = this.tables[event]
      }
      console.log(this.data.tables[0])
    },
    
    saveTable(){
      this.$http
      .post("api/table/", JSON.stringify(this.data.tables[0]), {
          headers: {
            // Overwrite Axios's automatically set Content-Type
            'Content-Type': 'application/json'
          }
        }
      )
      .then((response) => {
        this.alert = true
        console.log(response)
      })
    }

  }

}
</script>

<style>

</style>