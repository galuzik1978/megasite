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
          Скомпоновать форму
        </v-tab>
        <v-tab>
          <v-icon left>
            mdi-table-arrow-down
          </v-icon>
          Создать таблицу
        </v-tab>
        <v-tab>
          <v-icon left>
           mdi-clipboard-edit-outline
          </v-icon>
          Управление дефектами
        </v-tab>

        <v-tab>
          <v-icon left>
           mdi-clipboard-edit-outline
          </v-icon>
          Управление документами
        </v-tab>

        <v-tab-item>
          <create_form
            :form=all_forms[form_index]
            :tables=all_tables
          ></create_form>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-title class="text-center justify-center">
              Сформируйте все столбцы и строки таблицы контроля
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
            <v-card-text>
              <custom_table
                :headers="table_headers"
                :items="table_items"
              >
              </custom_table>
              <v-btn color="warning" @click="addCol({headers:table_headers, items:table_items})">Добавить столбец таблицы</v-btn>
            </v-card-text>
            <v-card-subtitle>
              Содержимое таблицы
            </v-card-subtitle>
            <v-card-text>
              <custom_table
                :headers="table_items"
                :items="items"
                :creating=true
              >
              </custom_table>
              <v-btn color="warning" @click="addCol({headers:table_items, items:items})">Добавить строку таблицы</v-btn>
            </v-card-text>
          </v-card>
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
export default {

  components:{
    custom_table,
    create_form
  },

  data:() => ({
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
            'none',
            'start',
            'center',
            'end'
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
            'none',
            'bool',
            'select',
            'actions',
            'rows_num',
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
            'none',
            'del',
            'add',
          ],
          editable: true
        },
      ],
    table_items:[],
   
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
      row.select_items = []
      table.items.push(
        row
      )
    },

    addRow(row, table){
      let tmp = []
      for (let i in row){
        tmp[i] = row[i]
      }
      table.push(tmp)
      console.log(this.all_documents)
    }

  },

  created(){
    this.reasons_header[2].select_items = this.all_documents
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