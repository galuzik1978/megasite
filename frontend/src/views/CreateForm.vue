<template>
  <div>
    <v-card color="basil">
      <v-card-title class="text-center justify-center py-6">
          Создать новую форму протокола
      </v-card-title>
  
      <v-tabs
        background-color="transparent"
        color="basil"
        grow
        v-model="tab"
      >
        <v-tab>
          <v-icon left>
            mdi-playlist-plus
          </v-icon>
          Формы
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-table-arrow-down
          </v-icon>
          Таблицы
        </v-tab>
        <v-tab>
          <v-icon left>
           mdi-clipboard-edit-outline
          </v-icon>
          Дефекты
        </v-tab>

        <v-tab>
          <v-icon left>
           mdi-clipboard-edit-outline
          </v-icon>
          Документы
        </v-tab>

        <v-tab-item>
          <create_form
            :form=all_forms
            :tables=tables
          ></create_form>
        </v-tab-item>
        <v-tab-item>
          <create_table
            :data=data
            :tables=all_tables
          ></create_table>          
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-title class="text-center justify-center">
              Введите все контролируемые пункты
            </v-card-title>
            <v-row justify='center'>
              <v-col
                cols=6
              >
                <v-text-field
                  label="Введите наименование таблицы"
                >
                </v-text-field>
              </v-col>
            </v-row>
            <v-card-subtitle>
              Заголовок таблицы
            </v-card-subtitle>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-card-title class="text-center justify-center">
              Введите основные нормативные документы
            </v-card-title>
            <v-card-text>
              <custom_table
                :items="all_documents"
                :headers="documents_header"
                data-date-picker="activated"
              >
              </custom_table>
              <v-btn color="warning" @click="addCol({headers:documents_header, items:all_documents})">Добавить строку таблицы</v-btn>
            </v-card-text>
            <v-card-title class="text-center justify-center">
              Введите контролируемые пункты по каждому документу
            </v-card-title>
            <v-card-text>
              <custom_table
                :items="all_reason"
                :headers="reasons_header"
                data-date-picker="activated"
                item_text="name"
              >
              </custom_table>
              <v-btn color="warning" @click="addCol({headers:reasons_header, items:all_reason})">Добавить строку таблицы</v-btn>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
import custom_table from '../components/CustomTable'
import create_form from '../components/CreateForm'
import create_table from '../components/CreateTable'
export default {

  components:{
    custom_table,
    create_form,
    create_table
  },

  data:() => ({
    
    data: {
      object:{
        reg_num: 'Регистрационный номер',
        form:{
          name: ''
        }
      },
      tables:[
        {
          header:[],
          expanded:[],
          collapse:true,
          annex_table:[],
          dataset:[],
        }
      ],
      annex_table:[],
    },
    annex_table:[],
    images:[],

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
          text: 'text',
          align: 'start',
          sortable: false,
          value: 'text',
      },
      {
          text: 'value',
          align: 'start',
          sortable: false,
          value: 'value',
      },
    ],

    tab: null,
    item: [],
    current_table_headers_item:[],
    all_forms: [
      {
        id:0,
        tables:[],
        creating:true
      }
    ],
    all_tables: [
      {
        id:1,
        phrasing: "Внешний осмотр",
        document: "ГОСТ Р 53780"
      },
      {
        id:2,
        phrasing: "Сопротивление изоляции",
        document: "ГОСТ Р 53780"
      },
      {
        id:3,
        phrasing: "Контроль заземления",
        document: "ГОСТ Р 53780"
      },
    ],
    all_defects:[],
    all_documents:[],
    all_values:[],
    all_reason:[],
    form_index: 0,
    empty_form:{
      id:null,
      name:"",
      tables:[],
    },
    empty_table:{
      id:null,
      name:"",
      headers:[],
      items:[],
    },
    empty_defect:{
      id:null,
      name:"",
      phrasing:"",
      reason:[]
    },
    empty_document:{
      id:null,
      name:"",
    },
    empty_reason:{
      id:null,
      name:"",
      document:null,
      point:"",
      phrasing:""
    },
   
    items:[],
    tables:[
      {
        phrasing: "Внешний осмотр",
        document: "ГОСТ Р 53780"
      },
      {
        phrasing: "Сопротивление изоляции",
        document: "ГОСТ Р 53780"
      },
      {
        phrasing: "Контроль заземления",
        document: "ГОСТ Р 53780"
      },
    ],
    tables_header: [
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%'
      },
      { text: 'Наименование контроля', value: 'phrasing', width: '30%' },
      { text: 'Нормативная документация, устанавливающая требования', value: 'document', width: '30%' },
      { text: '', value: 'delete_action', width: '5%' },
    ],
    documents_header: [
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%',
        type: 'rows_num',
      },
      { text: 'Наименование документа', value: 'name', width: '30%', editable:true },
    ],
    reasons_header:[
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%',
        type: 'rows_num',
      },
      { text: 'Краткое наименование', value: 'name', width: '30%', editable:true },
      { 
        text: 'Наименование документа', 
        value: 'document', 
        width: '30%', 
        editable:true, 
        type: 'select',
        select_items:[
          'none',
          'start',
          'center',
          'end'
        ],
      },
      { text: 'Пункт документа', value: 'point', width: '30%', editable:true },
      { text: 'Формулировка', value: 'phrasing', width: '30%', editable:true },
    ],
    defects_header:[
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%'
      },
      { text: 'Наименование', value: 'name', width: '30%' },
      { text: 'Формулировка', value: 'phrasing', width: '30%' },
      { text: 'Основание', value: 'reason', width: '30%' },
    ],
  }),

  props:{
    
  },

  methods:{

    AddDefect(){
      return null
    },

    delete_table_from_form(item){
      let editedIndex = this.item.indexOf(item)
      this.item.splice(editedIndex, 1)
    },

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
        [event.items[event.i-1], event.items[event.i]] = [event.items[event.i], event.items[event.i-1]]
        console.log('up')
        console.log(event)
        event.items.splice()
      }
    },

    sorting_down(event){
      if (event.i < (event.items.length - 1)){
        [event.items[event.i+1], event.items[event.i]] = [event.items[event.i], event.items[event.i+1]]
        console.log('down')
        console.log(event)
        event.items.splice()
      }
    },

    sorting_delete(event){
      console.log('delete')
      console.log(event)
      event.items.splice(event.i, 1)
    }

  },

  created(){
    this.reasons_header[2].select_items = this.all_documents
  },

  mounted(){
    let v = this
    this.$http
    .get("api/form/", {params: this.$attrs})
    .then((response) => {
      v.all_forms = response.data
    })
    this.$http
    .get("api/table/", {params: this.$attrs})
    .then((response) => {
      v.all_tables = response.data
      v.tables = []
      for (let table of v.all_tables){
        v.tables.push({id:table.id, name:table.name})
      }
    })
  },

}
</script>

<style scoped>
 div >>> .multiple_select .v-select__selections{
   display:none;
 }
 div >>> .v-data-table__expanded.v-data-table__expanded__content{
   background-color: gainsboro;
 }
 div >>> .table-extend{
   background-color: gainsboro;
 }
div >>> .grid_table{
  width: 100%;
}
</style>