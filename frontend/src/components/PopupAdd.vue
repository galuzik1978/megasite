<template>
  <div>
    
    <!-- Всплывающее окно добавления нового контакта -->
    <v-dialog
      v-model="dialog"
      width="800px"
      persistent
    >
      <v-card>
        <v-card-title class="grey darken-2">
          {{ content.title }}
        </v-card-title>
        <v-list-item-subtitle>
          {{ save_err }}
        </v-list-item-subtitle>
        <v-container>
          <v-row class="mx-2">
            <template v-for="(field, index) in fields">
              <v-col :cols=field.width :key=field.id :style="{ display: field.width>0 ? 'block': 'none' }">
                
                <ApiSelect 
                  v-if="field.type=='select'"
                  :field=fields[index] 
                  @getSelect="getApiSelect"
                  :key=fields[index].name
                  v-model=fields[index].value
                ></ApiSelect>

                <v-menu
                  v-else-if="field.type=='date'"
                  v-model="menu[index]"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                  :key=fields[index].name
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model=field.value
                      label="Выбери дату"
                      :prepend-icon=field.icon
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model=fields[index].value @input="menu[index] = false"></v-date-picker>
                </v-menu>

                <v-textarea
                  v-else-if="field.type=='textarea'"
                  v-model=fields[index].value
                  :label=field.text
                  :key=fields[index].name
                ></v-textarea>

                <v-file-input 
                  v-else-if="field.type=='file'"
                  show-size
                  :label=field.text
                  :key=fields[index].name
                  v-model=fields[index].value
                ></v-file-input>

                <input 
                  v-else-if="field.type=='hidden'"
                  type="hidden"
                  v-model=fields[index].value
                  :key=fields[index].name
                >

                <v-text-field
                  v-else
                  :prepend-icon=field.icon 
                  :placeholder=field.text
                  v-model=fields[index].value
                  :type=field.type
                  @change="handleFunctionCall(field.callback, $event)"
                  :key=fields[index].name
                  :error-messages=fields[index].error
                  :success-messages=fields[index].success
                ></v-text-field>

              </v-col>
            </template>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="close"
          >Отмена</v-btn>
          <v-btn
            text
            @click="saveItem"
          >Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ApiSelect from "../components/ApiSelect"
export default {
  name: 'PopupAdd',
  components:{
    ApiSelect
  },

  props:{
    dialog:{
      type: Boolean,
      required: true
    },
    content: {
      type: Object,
      default: function () {
        return {
          title: 'Добавить контакт',
          fields: [
            {
              type: 'text',
              text: 'Имя',
              width: 12,
              icon: 'fa fa-user',
              name: "name",
              value: ""
            },
            {
              type: 'select',
              text: 'Компания',
              width: 6,
              icon: 'mdi-mail',
              name: 'company',
              value: "",
              items: [
                'Компания 1',
                'Компания 2',
                'Компания 3'
              ]
            },
            {
              type: 'text',
              text: 'Должность',
              width: 6,
              name: 'role',
              value: ""
            },
            {
              type: 'email',
              text: 'E-mail',
              width: 12,
              icon: 'mdi-mail',
              name: 'email',
              value: ""
            },
            {
              type: 'text',
              text: 'Телефон',
              width: 6,
              icon: 'mdi-phone',
              name: 'phone',
              value: ""
            },
            {
              type: 'date',
              text: 'Дата',
              width: 6,
              icon: 'mdi-calendar',
              name: 'date',
              value: ""
            },
            {
              type: 'textarea',
              text: 'Содержание',
              width: 12,
              icon: 'mdi-clipboard-text',
              name: 'content',
              value: ""
            },
            {
              type: 'file',
              text: 'Приложение',
              width: 12,
              icon: 'mdi-clipboard-text',
              name: 'annex',
              value: ""
            },
          ]
        }
      }
    },

    url: {
      type: String,
    }
  },

  computed: {
  },

  data: () => ({
    date: new Date().toISOString().substr(0, 10),
    menu: [],
    fields:[],
    err:"",
    save_err:""
  }),

  methods: {

    saveItem: function() {
      let data = {};
      let formData = new FormData();
      for (var field in this.fields) {
        if (this.fields[field].value){
          data[field] = this.fields[field].value
          formData.append(field, this.fields[field].value)     
        }
      }
      let v = this
      this.$store.dispatch('save_item', {'url':this.url, 'data':formData})
      .then(() => {
        v.$emit('select_update')
        v.close()
      })
      .catch(error => {
        v.save_err = error.response.data
      })
    },

    close: function() {
      this.$emit('closeItem', this.fields)
      this.save_err = ""
    },

    updateItem: function(){
      return this.lazyValue
    },
    
    getApiSelect: function(Val){
      return Val
    },

    edit: function(){
      this.close()
    },

    handleFunctionCall(functionName, event) {
      if (functionName != undefined) {
        this[functionName](event)
      }
    },

    inn_request(event){
      let v = this
      this.$http.get('api/innrequest/', {params:{inn:event}})
      .then((resp) => {
        v.fields["full_name"].value = resp.data.full_name
        v.fields["head"].value = resp.data.head
        v.fields["head_last_name"].value = resp.data.head_last_name
        v.fields["head_name"].value = resp.data.head_name
        v.fields["head_surname"].value = resp.data.head_surname
        v.fields["type_customer"].value = resp.data.type_customer
        v.fields["ogrn"].value = resp.data.ogrn
        v.fields["kpp"].value = resp.data.kpp
        v.fields["inn"].value = resp.data.inn
        v.fields["inn"].error = ""
        v.fields["inn"].success = 'Обновлено значение. Найдено ' + resp.data.len +  ' субъектов.'
        console.log("err=" + v.fields["inn"].error)
        v.fields["inn"].name = "inn1"
        v.fields["inn"].name = "inn"
      })
      .catch(error => {
        v.fields["inn"].error = error.response.data
        v.fields["inn"].success = ""
        v.fields["inn"].name = "inn1"
        v.fields["inn"].name = "inn"
        console.log("err=" + v.fields["inn"].error) 
      });
      
    }
  },
  
  updated(){
    console.log("updated")
    this.fields = this.content.fields
  }
}
</script>

<style>
.v-list-item__subtitle{
  color:red;
  text-align: center;
}
</style>