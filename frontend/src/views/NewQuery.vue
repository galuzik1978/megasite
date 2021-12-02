 <template>
      <v-card> 
        <v-card-title width="100%" class="blue lighten-2 text-center" >
          Заполните заявку на выполнение работ
        </v-card-title>
        <v-card>
          <v-card-text>
            <h3>Реквизиты заказчика:</h3>
            <h3 class="text-center"> {{customer}} </h3>
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
              <v-col cols=6 v-if="ressived">
                <v-text-field 
                  v-model="full_name"
                  label="Полное название организации"
                ></v-text-field>
              </v-col>
              <v-col cols=6 v-if="ressived">
                <v-text-field 
                  v-model="head"
                  label="Руководитель организации"
                ></v-text-field>
              </v-col>
              <v-col cols=6 v-if="ressived">
                <v-text-field 
                  v-model="type_customer"
                  label="Тип заказчика"
                ></v-text-field>
              </v-col>
              <v-col cols=4 v-if="ressived">
                <v-text-field 
                  v-model="head_last_name"
                  label="Фамилия руководителя"
                ></v-text-field>
              </v-col>
              <v-col cols=4 v-if="ressived">
                <v-text-field 
                  v-model="head_name"
                  label="Имя руководителя"
                ></v-text-field>
              </v-col>
              <v-col cols=4 v-if="ressived">
                <v-text-field 
                  v-model="head_surname"
                  label="Отчество руководителя"
                ></v-text-field>
              </v-col>
              <v-col cols=6 v-if="ressived">
                <v-text-field 
                  v-model="ogrn"
                  label="ОГРН"
                ></v-text-field>
              </v-col>
              <v-col cols=6 v-if="ressived">
                <v-text-field 
                  v-model="kpp"
                  label="КПП (при наличии)"
                ></v-text-field>
              </v-col>
              <v-col cols=12 v-if="ressived">
                <v-text-field 
                  v-model="address"
                  label="Юридический адрес"
                ></v-text-field>
              </v-col>
              <v-col cols=12 v-if="ressived">
                <v-text-field 
                  v-model="post_address"
                  label="Почтовый адрес"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        <v-card-title width="100%" class="blue lighten-2 text-center" >
          Выберите вид выполняемых работ
        </v-card-title>
        <v-select
          v-model="work_select"
          :items="work_items"
          item-text="name"
          :rules="[v => !!v || 'Выберите вид работы']"
          label="Вид работы"
          required
          return-object
        >
        </v-select>
        <v-card
          v-if="work_select==work_items[0]"
        >
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
                  @click="add_row(table_rows, 0)"
                  color="primary"
                >
                  Добавить объект
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  @click="del_row(table_rows, 0)"
                  color="success"
                >
                  Удалить объект
                </v-btn>
                <v-spacer></v-spacer>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
        <v-card
          v-if="work_select==work_items[1]"
        >
          <v-card-text>
            <v-form
              ref="form1"
              v-model="valid1"
              lazy-validation
              id="form1"
            >
              <h3>Введите адрес расположения контролируемого оборудования:</h3>
              <v-row>
                <v-col cols=12>
                  <v-text-field 
                    v-model="obj_address"
                    label="Адрес контролируемого объекта"
                  ></v-text-field>
                </v-col>
              </v-row>
              <h3>Выберите необходимые испытания:</h3>
              <v-checkbox
                v-model="selected_controls"
                :label="control"
                :value="control"
                v-for="control in controls" :key=control
              ></v-checkbox>
            </v-form>
          </v-card-text>
        </v-card>
        <v-card
          v-if="work_select==work_items[2]"
        >
          <v-card-text>
            <v-form
              ref="form2"
              v-model="valid2"
              lazy-validation
              id="form2"
            >
              <h3>1)Наименование оборудования (объектов)</h3>
              <v-checkbox
                v-model="selected_objects"
                :label="object"
                :value="object"
                v-for="object in objects" :key=object
              ></v-checkbox>
              <h3>2)Вид (метод) неразрушающего контроля</h3>
              <v-checkbox
                v-model="selected_methods"
                :label="method"
                :value="method"
                v-for="method in methods" :key=method
              ></v-checkbox>
              <table class="grid_table">
                <thead>
                  <tr>
                    <th>№ п/п</th>
                    <th>Адрес нахождения объекта контроля</th>
                    <th>Наименование объекта контроля</th>
                    <th>Наименование элементов подвергаемых контролю</th>
                    <th>Объем (количество)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, i) in table1_rows" :key="'row_table1' + i">
                    <td>{{ i+1 }}</td>
                    <td><v-text-field v-model="row.address"></v-text-field></td>
                    <td><v-text-field v-model="row.object"></v-text-field></td>
                    <td><v-text-field v-model="row.element"></v-text-field></td>
                    <td><v-text-field v-model="row.count"></v-text-field></td>
                  </tr>
                </tbody>
              </table>
              <v-row class="pa-md-4">
                <v-spacer></v-spacer>
                <v-btn
                  @click="add_row(table1_rows, 1)"
                  color="primary"
                >
                  Добавить объект
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  @click="del_row(table1_rows, 1)"
                  color="success"
                >
                  Удалить объект
                </v-btn>
                <v-spacer></v-spacer>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
        <v-btn class="my-6"
          color="primary"
          @click="save_blank"
          width="100%"
          elevation="6"
        >Сохранить бланк заявки</v-btn>
      </v-card>
 </template>
 
 <script>
 export default {

  data: () => ({

    valid: true,
    valid1: true,
    valid2: true,

    customer: "Введите ИНН или название своей организации",

    type_work_select: null,

    type_work_items: [
      'периодического технического освидетельствования',
      'полного технического освидетельствования',
      'отработавшего(их) назначенный срок службы 25 лет',
    ],

    work_select: null,

    work_items: [
      'проведение оценки соответствия лифта требованиям технического регламента Таможенного союза «Безопасность лифтов»',
      'проведение приемо-сдаточных, эксплуатационных испытаний электрооборудования до 1000в',
      'проведение неразрушающего контроля',
    ],

    selected_controls:[],

    controls:[
      "Проверка соответствия смонтированной схемы электроустановки требованиям нормативно-технической документации (визуальный осмотр),",
      "Проверка наличия цепи между заземленной электроустановкой и элементами заземленной электроустановки (непрерывности защитных проводников),",
      "Измерение сопротивления заземляющих устройств,",
      "Измерение сопротивления изоляции кабельных линий, электродвигателей, электрических аппаратов, вторичных цепей и электропроводок напряжением до 1000 вольт,",
      "Проверка петли «фаза-нуль» в электроустановках до 1000 вольт с системой ТN(измерение полного сопротивления петли «фаза-нуль» с последующим определением тока к.з.)",
      "Проверка параметров устройств защитного отключения (УЗО),",
      "Проверка и испытание расцепителей автоматических выключателей,",
      "Испытания устройств автоматического включения резервного питания (АВР),",
      "Измерение показателей качества электроэнергии в системах электроснабжения общего назначения."
    ],

    selected_objects:[],

    objects:[
      "Системы газоснабжения (газораспределения)",
      "Подъёмные сооружения",
      "Оборудование нефтяной и газовой промышленности",
      "Оборудование взрывопожароопасных и химически опасных производств",
      "Здания и сооружения (строительные объекты)",
      "Металлические конструкции",
      "Бетонные и железобетонные конструкции",
    ],

    selected_methods:[],

    methods:[
      "Ультразвуковой (дефектоскопия, толщинометрия)",
      "Магнитный (метод магнитной памяти металла)",
      "Вихретоковый (только для подъемных сооружений)",
      "Проникающими веществами (капиллярный)",
      "Тепловой (только для зданий и сооружений)",
      "Визуальный н измерительный",
      "Прочность бетона (метод ударного импульса)",
    ],

    iframeSrc:"",
    obj_address:"",
    table1_rows: [{
        address:"",
        object: "",
        element: "",
        count:"",
      }],

    row1_shape:[{
        address:"",
        object: "",
        element: "",
        count:"",
    }],

    table_rows: [{
        address:"",
        reg: "",
        year_of_commission: null,
        type:"",
        capacity:"",
        floors:"",
        last_verife:"",
        dpicker: false,
        type_lift:{
          name:""
        }
      }],

    row_shape:[
      {
        address:"",
        reg: "",
        year_of_commission: null,
        type:"",
        capacity:"",
        floors:"",
        last_verife:"",
        dpicker: false,
        type_lift:{
          name:""
        }
      },
      {
        address:"",
        object: "",
        element: "",
        count:"",
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
    ressived: false,
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
          this.type_work_select = data.form
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

    add_row(table, i){
      let tmp = this.deepClone(this.row_shape[i])
      table.push(tmp)
    },

    del_row(table){
      table.pop()
    },

    inn_request(event){
      let v = this
      this.$http.get('api/innrequest/', {params:{inn:event}})
      .then((resp) => {
        v.id = Number(this.id)
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
        v.ressived = true
        v.customer = "Откорректируйте или заполните поля или попробуйте ввести ИНН еще раз. Если все заполнено верно, продолжайте заполнять форму"
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