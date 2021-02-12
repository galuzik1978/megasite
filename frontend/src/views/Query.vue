 <template>
      <v-card> 
        <v-card-title width="100%" class="blue lighten-2 text-center" >
          Заявка на проведение оценки соответствия лифта требованиям технического регламента Таможенного союза «Безопасность лифтов»
        </v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
            id="form"
          >
            <h3>Просим Вас провести оценку соответствия в форме</h3>
            <v-select
              v-model="type_work_select"
              :items="type_work_items"
              item-text="name"
              :rules="[v => !!v || 'Выберите форму оценки']"
              label="Форма оценки"
              required
              return-object
            ></v-select>
            <table class="grid_table">
              <thead>
                <tr>
                  <th>№ п/п</th>
                  <th>Адрес установки лифта (ов)</th>
                  <th>Рег.№</th>
                  <th>Год ввода</th>
                  <th>Тип</th>
                  <th>Грузоподъемность</th>
                  <th>Кол-во остановок</th>
                  <th>Месяц и год последнего освидетельствования</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, i) in table_rows" :key="'row_table' + i">
                  <td>{{ i+1 }}</td>
                  <td><v-textarea v-model="row.address"></v-textarea></td>
                  <td><v-text-field v-model="row.reg_num"></v-text-field></td>
                  <td>
                    <v-select
                      v-model="row.mf_year"
                      :items="years"
                      :rules="[v => !!v || 'Выберите год ввода объекта в эксплуатацию']"
                      required
                    >
                    </v-select>
                  </td>
                  <td><v-text-field v-model="row.type_lift.name"></v-text-field></td>
                  <td><v-text-field v-model="row.capacity"></v-text-field></td>
                  <td><v-text-field v-model="row.floors"></v-text-field></td>
                  <td>
                    <v-col>
                      <v-menu
                        v-model="row.dpicker"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="row.date_exam"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="row.date_exam"
                          @input="row.dpicker = false"
                          locale="ru"
                          type="month"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                  </td>
                </tr>
              </tbody>
            </table>
            <v-row class="pa-md-4">
              <v-spacer></v-spacer>
              <v-btn
                @click="add_row"
                color="primary"
              >
                Добавить объект
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                @click="del_row"
                color="success"
              >
                Удалить объект
              </v-btn>
              <v-spacer></v-spacer>
            </v-row>
            <v-card>
              <v-card-text>
                <h3>Реквизиты заказчика:</h3>
                <v-row>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="inn"
                      label="Введите ИНН"
                      @change="inn_request"
                      :error-messages=inn_error
                      :success-messages=inn_success
                    ></v-text-field>
                  </v-col>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="full_name"
                      label="Полное название организации"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="head"
                      label="Руководитель организации"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="type_customer"
                      label="Тип заказчика"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=4>
                    <v-text-field 
                      v-model="head_last_name"
                      label="Фамилия руководителя"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=4>
                    <v-text-field 
                      v-model="head_name"
                      label="Имя руководителя"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=4>
                    <v-text-field 
                      v-model="head_surname"
                      label="Отчество руководителя"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="ogrn"
                      label="ОГРН"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=6>
                    <v-text-field 
                      v-model="kpp"
                      label="КПП (при наличии)"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=12>
                    <v-text-field 
                      v-model="address"
                      label="Юридический адрес"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=12>
                    <v-text-field 
                      v-model="post_address"
                      label="Почтовый адрес"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-card-text>
              </v-card>
              <v-card class="my-6">
                <v-card-text>
                  <h3>Банковские реквизиты:</h3>
                  <v-row>
                    <v-col cols=6>
                      <v-text-field 
                        v-model="bik"
                        label="БИК"
                      ></v-text-field>
                    </v-col>
                    <v-col cols=6>
                      <v-text-field 
                        v-model="bank"
                        label="Наименование банка"
                      ></v-text-field>
                    </v-col>
                    <v-col cols=6>
                      <v-text-field 
                        v-model="account"
                        label="Расчетный счет"
                      ></v-text-field>
                    </v-col>
                    <v-col cols=6>
                      <v-text-field 
                        v-model="korr_account"
                        label="Корр.счет"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            
            <v-btn class="my-6"
              color="primary"
              @click="save_blank"
              width="100%"
              elevation="6"
            >Сохранить бланк заявки</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
 </template>
 
 <script>
 export default {

  data: () => ({

    valid: true,

    type_work_select: null,

    type_work_items: [
      'периодического технического освидетельствования',
      'полного технического освидетельствования',
      'отработавшего(их) назначенный срок службы 25 лет',
    ],

    iframeSrc:"",
    
    table_rows: [],

    row_shape:[
      {
        address:"",
        reg: "",
        year_of_commission: null,
        type:"",
        capacity:"",
        floors:"",
        last_verife:"",
        dpicker: false
      }
    ],

    last_verife: new Date().toISOString().substr(0, 10),
    
    inn:"",
    full_name:"",
    head:"",
    head_last_name:"",
    head_name:"",
    head_surname:"",
    type_customer:"",
    ogrn:"",
    kpp:"",
    address:"",
    post_address:"",
    bik:"",
    bank:"",
    account:"",
    korr_account:"",
    inn_error:"",
    inn_success:"",
  }),

  computed:{

    year(){
      return (new Date().getFullYear())
    },

    years(){
      return [...Array.from(Array(120).keys(),x=>String(this.year-x))]
    },

    url(){
      return "api/workrequest/" + this.id + "/"
    }

  },

  props:{
    id: Number
  },

  watch: {
    id: {
      immediate: true,
      handler(){
        this.$http
        .get(this.url)
        .then((response) => {
          let data = response.data
          console.log(this.items)
          this.full_name = data.contract.customer.full_name
          this.inn = data.contract.customer.inn
          this.head = data.contract.customer.head
          this.head_name = data.contract.customer.head_name
          this.head_surname = data.contract.customer.head_surname
          this.head_last_name = data.contract.customer.head_last_name
          this.ogrn = data.contract.customer.ogrn
          this.kpp = data.contract.customer.kpp
          this.type_customer = data.contract.customer.type_customer.name
          this.address = data.contract.customer.legal_address
          this.post_address = data.contract.customer.post_address
          this.bik = data.contract.customer.bic
          this.bank = data.contract.customer.bank
          this.account = data.contract.customer.account
          this.korr_account = data.contract.customer.cor_account,
          this.type_work_items = data.all_forms
          this.table_rows = data.objects
        })
      }
    }
  },

  methods:{
    
    deepClone(obj) {
      const clObj = {};
      for(const i in obj) {
        if (obj[i] instanceof Object) {
          clObj[i] = this.deepClone(obj[i]);
          continue;
        }
        clObj[i] = obj[i];
      }
      return clObj;
    },

    add_row(){
      //let tmp = this.deepClone(this.row_shape)
      this.table_rows.push({})
    },

    del_row(){
      this.table_rows.pop()
    },

    inn_request(event){
      let v = this
      this.$http.get('api/innrequest/', {params:{inn:event}})
      .then((resp) => {
        v.id = this.id
        v.full_name = resp.data.full_name
        v.head = resp.data.head
        v.head_last_name = resp.data.head_last_name
        v.head_name = resp.data.head_name
        v.head_surname = resp.data.head_surname
        v.type_customer = resp.data.type_customer.name
        v.ogrn = resp.data.ogrn
        v.kpp = resp.data.kpp
        v.inn = resp.data.inn
        v.address = resp.data.address
        v.inn_error = ""
        v.inn_success = 'Обновлено значение. Найдено ' + resp.data.len +  ' субъектов.'
        console.log("err=" + v.inn_error)
      })
      .catch(error => {
        v.inn = error.response.data
        v.inn_success = ""
        console.log("err=" + v.inn_error) 
      });
      
    },

    save_blank(){
      var fileDownload = require('js-file-download');
      let formData = new FormData();
      formData.append('inn', this.inn)
      formData.append('full_name',this.full_name)
      formData.append('head',this.head)
      formData.append('head_last_name',this.head_last_name)
      formData.append('head_name',this.head_name)
      formData.append('head_surname',this.head_surname)
      formData.append('type_customer',this.type_customer)
      formData.append('ogrn',this.ogrn)
      formData.append('kpp',this.kpp)
      formData.append('address',this.address)
      formData.append('post_address',this.post_address)
      formData.append('bik',this.bik)
      formData.append('bank',this.bank)
      formData.append('account',this.account)
      formData.append('korr_account',this.korr_account)
      formData.append('table_rows', JSON.stringify(this.table_rows))
      formData.append('form', JSON.stringify(this.type_work_select))
      
      this.$http.post(this.url, formData)
      .then((response) => {
        this.items = response.data
        fileDownload(response.data, "Основные функции.ods");
      })

    }

  },

  mounted(){
    this.add_row()
  }

 }
 </script>
 
 <style>
.grid_table{
  border-collapse: collapse; 
  line-height: 1.1;
}
.grid_table td, .grid_table th {
  padding: 3px; /* Поля вокруг содержимого таблицы */
  border: 1px solid black; /* Параметры рамки */
}
 </style>