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
                  :key=fields[index].name
                  :value=fields[index].value
                  @input="changeSelect(field, $event)"
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
                      :label=field.text
                      :prepend-icon=field.icon
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model=fields[index].value @input="menu[index] = false, cnangeItem(fields[index])"></v-date-picker>
                </v-menu>

                <v-textarea
                  v-else-if="field.type=='textarea'"
                  v-model=fields[index].value
                  :label=field.text
                  :key=fields[index].name
                  @change="cnangeItem(fields[index])"
                ></v-textarea>

                <v-file-input 
                  v-else-if="field.type=='file' && !update"
                  show-size
                  :label=field.text
                  :key=fields[index].name
                  v-model=fields[index].value
                  @change="cnangeItem(fields[index])"
                ></v-file-input>
                
                <a 
                  v-else-if="field.type=='file' && update"
                  show-size
                  :label=field.text
                  :key=fields[index].name
                  :href=fields[index].value
                  target="_blank"
                >{{ fields[index].value }}</a>

                <input 
                  v-else-if="field.type=='hidden'"
                  type="hidden"
                  v-model=fields[index].value
                  :key=fields[index].name
                  @change="cnangeItem(fields[index])"
                >

                <v-text-field
                  v-else
                  :prepend-icon=field.icon 
                  :placeholder=field.text
                  v-model=fields[index].value
                  :type=field.type
                  @change="handleFunctionCall(field.callback, $event), cnangeItem(fields[index])"
                  :key=fields[index].name
                  :error-messages=fields[index].error
                  :success-messages=fields[index].success
                ></v-text-field>

              </v-col>
            </template>
          </v-row>
        </v-container>

        <v-card-actions v-if="actions && update"> 
          <template v-for="(action, index) in actions"> 
            <v-spacer 
              :key="'spacer' + index"
            ></v-spacer> 
            <v-btn 
              elevation="8" 
              :color="action.color"
              @click="handlerClickEvent(action.url)"
              :key="'btn' + index"
            > 
              <v-icon
                left
              >
                {{ action.icon }}
              </v-icon>
            {{ action.text }}</v-btn>
          </template>
          <v-spacer></v-spacer>
        </v-card-actions>

        <v-card-actions v-else>
          <v-spacer></v-spacer>
          <v-btn
            elevation="8" 
            @click="close"
          >Отмена</v-btn>
          <v-btn v-if="update"
            color="primary"
            @click="updateItem"
            elevation="8" 
          >Обновить</v-btn>
          <v-btn v-else
            color="primary"
            @click="saveItem"
            elevation="8" 
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
    },

    update:{
      type: Boolean,
      default: false
    },
    
    actions: {
      type: Object,
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
      let formData = new FormData();
      for (var field in this.fields) {
        if (this.fields[field].value){
          if(typeof this.fields[field].value == 'object' && this.fields[field].type != 'file'){
            formData.append(field, JSON.stringify(this.fields[field].value))
          } else{
            formData.append(field, this.fields[field].value)
          }
        }
      }
      let v = this
      this.$store.dispatch('save_item', {'url':this.url, 'data':formData})
      .then(() => {
        v.$emit('itemsChanged')
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
      let formData = new FormData();
      for (var field in this.fields) {
        if (this.fields[field].change){
          formData.append(field, JSON.stringify(this.fields[field].value))     
        }
      }
      let v = this
      this.$store.dispatch('update_item', {'url':this.url, 'id':v.fields.id.value, 'data':formData})
      .then(() => {
        v.$emit('itemsChanged')
        v.close()
      })
      .catch(error => {
        v.save_err = error.response.data
      })
    },

    edit: function(){
      this.close()
    },

    handleFunctionCall(functionName, event) {
      if (functionName != undefined) {
        this[functionName](event)
      }
    },

    changeSelect(field, event){
      field.value= event
      this.cnangeItem(field)
    },

    cnangeItem(item){
      item.change = true
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
      
    },

    handlerClickEvent(url){
      if (url == undefined) {
        this.close()
      } else {
        let v = this
        this.$store.dispatch('action_handler', {'url': url, 'id': v.fields.id.value})
        .then(() => {
          v.$emit('itemsChanged')
          v.close()
        })
        .catch(error => {
          v.save_err = error.response.data
        })
      }

    }

  },
  
  updated(){
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