 <template>
      <v-card> 
        <v-card-title width="100%" class="blue lighten-2 text-center" >
          Заполните заявку на выполнение работ <v-spacer></v-spacer> 
          <v-icon v-if=collapse @click="collapse = false">mdi-window-maximize</v-icon>
          <v-icon v-else @click="collapse = true">mdi-window-minimize</v-icon>
        </v-card-title>
        <v-card-text v-if="!collapse">
          <v-card >
            <v-card-text>
              <h3>Реквизиты заказчика:</h3>
              <h3 class="text-center"> {{customer}} </h3>
              <v-row>
                <v-col cols=12>
                  <v-autocomplete 
                    v-model="lead.customer"
                    :items="items"
                    :loading="isLoading"
                    :search-input.sync="search"
                    @input="input_customer"
                    color="black"
                    hide-no-data
                    hide-selected
                    item-text="Description"
                    item-value="data.inn"
                    label="ИНН или название компании"
                    placeholder="Начните вводить для поиска"
                    prepend-icon="mdi-database-search"
                    return-object
                  ></v-autocomplete>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.full_name"
                    label="Полное название организации"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.head"
                    label="Руководитель организации"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.type_customer"
                    label="Тип заказчика"
                  ></v-text-field>
                </v-col>
                <v-col cols=4 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.head_lastname"
                    label="Фамилия руководителя"
                  ></v-text-field>
                </v-col>
                <v-col cols=4 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.head_name"
                    label="Имя руководителя"
                  ></v-text-field>
                </v-col>
                <v-col cols=4 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.head_surname"
                    label="Отчество руководителя"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.ogrn"
                    label="ОГРН"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.kpp"
                    label="КПП (при наличии)"
                  ></v-text-field>
                </v-col>
                <v-col cols=12 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.legal_address"
                    label="Юридический адрес"
                  ></v-text-field>
                </v-col>
                <v-col cols=12 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.post_address"
                    label="Почтовый адрес"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.email"
                    label="Электронная почта"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.phone"
                    label="Номер телефона"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="ressived">
                  <v-text-field 
                    v-model="lead.customer.contact_name"
                    label="Контактное лицо"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-text>
              <v-card-title width="100%" class="blue lighten-2 text-center" >
                Выберите вид выполняемых работ
              </v-card-title>
              <v-select
                v-model="lead.work"
                :items="work_items"
                item-text="name"
                :rules="[v => !!v || 'Выберите вид работы']"
                label="Вид работы"
                required
                return-object
              >
              </v-select>
              <v-card
                v-if="lead.work==work_items[0]"
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
                      v-model="lead.type_work"
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
                        <tr v-for="(row, i) in lead.table_rows" :key="'row_table' + i">
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
                          <td><v-text-field v-model="row.type_lift"></v-text-field></td>
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
                        @click="add_row(lead.table_rows, 0)"
                        color="primary"
                      >
                        Добавить объект
                      </v-btn>
                      <v-spacer></v-spacer>
                      <v-btn
                        @click="del_row(lead.table_rows, 0)"
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
                v-if="lead.work==work_items[1]"
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
                          v-model="lead.obj_address"
                          label="Адрес контролируемого объекта"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <h3>Выберите необходимые испытания:</h3>
                    <v-checkbox
                      v-model="lead.controls"
                      :label="control"
                      :value="control"
                      v-for="control in controls" :key=control
                    ></v-checkbox>
                  </v-form>
                </v-card-text>
              </v-card>
              <v-card
                v-if="lead.work==work_items[2]"
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
                      v-model="lead.objects"
                      :label="object"
                      :value="object"
                      v-for="object in objects" :key=object
                    ></v-checkbox>
                    <h3>2)Вид (метод) неразрушающего контроля</h3>
                    <v-checkbox
                      v-model="lead.methods"
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
                        <tr v-for="(row, i) in lead.table1_rows" :key="'row_table1' + i">
                          <td>{{ i+1 }}</td>
                          <td><v-textarea v-model="row.address"></v-textarea ></td>
                          <td><v-text-field v-model="row.object"></v-text-field></td>
                          <td><v-text-field v-model="row.element"></v-text-field></td>
                          <td><v-text-field v-model="row.count"></v-text-field></td>
                        </tr>
                      </tbody>
                    </table>
                    <v-row class="pa-md-4">
                      <v-spacer></v-spacer>
                      <v-btn
                        @click="add_row(lead.table1_rows, 1)"
                        color="primary"
                      >
                        Добавить объект
                      </v-btn>
                      <v-spacer></v-spacer>
                      <v-btn
                        @click="del_row(lead.table1_rows, 1)"
                        color="success"
                      >
                        Удалить объект
                      </v-btn>
                      <v-spacer></v-spacer>
                    </v-row>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-text>
              <v-card-title width="100%" class="blue lighten-2 text-center">
                Введите банковские реквизиты для оформления договора
              </v-card-title>
              <v-row>
                <v-col cols=12>
                  <v-autocomplete 
                    v-model="lead.bank"
                    :items="banks"
                    :loading="banksisLoading"
                    :search-input.sync="banksearch"
                    @input="input_bank"
                    color="black"
                    hide-no-data
                    hide-selected
                    item-text="desc"
                    item-value="desc"
                    label="Реквизиты банка"
                    placeholder="Начните вводить для поиска"
                    prepend-icon="mdi-database-search"
                    return-object
                  ></v-autocomplete>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.name"
                    label="Наименование банка"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.bic"
                    label="БИК"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.kpp"
                    label="КПП"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.inn"
                    label="ОГРН"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.correspondent_account"
                    label="Корр. счет"
                  ></v-text-field>
                </v-col>
                <v-col cols=6 v-if="bank_ressived">
                  <v-text-field 
                    v-model="lead.bank.payment_account"
                    label="Расчетный счет"
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
        </v-card-text>
        <v-card-title v-if=sended width="100%" class="blue lighten-2 text-center" >
          Отправьте нам отсканированную заявку <v-spacer></v-spacer> 
          <v-icon v-if=collapse @click="collapse2 = false">mdi-window-maximize</v-icon>
          <v-icon v-else @click="collapse2 = true">mdi-window-minimize</v-icon>
        </v-card-title>
        <v-card-text v-if="!collapse2">
          1. Распечатайте полученную форму заявки на фирменном бланке Вашей организации<br>
          2. Проверьте правильность данных заявки, и, при необходимости, откорректируйте их<br>
          3. Подпишите заявку руководителем организации или доверенным лицом<br>
          4. Отсканируйте подписанную заявку и отправьте скан нам<br>
          <v-file-input></v-file-input>
          <v-dialog
            transition="dialog-top-transition"
            max-width="600"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                v-bind="attrs"
                v-on="on"
                width="100%"
                @click="send_blank">
                Отправить скан заявки
              </v-btn>
            </template>
            <template v-slot:default="dialog">
              <v-card>
                <v-toolbar
                  color="primary"
                  dark
                >Заявка успешно отправлена</v-toolbar>
                <v-card-text>
                  Спасибо за Ваше обращение!<br>
                  Мы свяжемся с Вами в ближайщее время
                </v-card-text>
                <v-card-actions class="justify-end">
                  <v-btn
                    text
                    @click="dialog.value = false"
                  >Закрыть</v-btn>
                </v-card-actions>
              </v-card>
            </template>
          </v-dialog>
        </v-card-text>
      </v-card>
 </template>
 
 <script>
 export default {
  
  data: () => ({

    descriptionLimit: 60,
    entries: [],
    bankentries:[],
    isLoading: false,
    banksisLoading: false,
    model: null,
    search: null,
    banksearch: null,
    count: null,
    bankscount: null,
    collapse: false,
    collapse2: true,
    sended: false,

    valid: true,
    valid1: true,
    valid2: true,

    lead:{
      customer: {},
      bank: {},
      type_work: null,
      work: [],
      controls: [],
      objects: [],
      methods: [],
      table1_rows: [{
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
        type_lift:"",
      }],
    },

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
      "Визуальный и измерительный",
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
        type_lift:"",
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
    bank_ressived: false,
  }),

  computed:{

    fields () {
      if (!this.inn) return []

      return Object.keys(this.inn).map(key => {
        return {
          key,
          value: this.inn[key] || 'n/a',
        }
      })
    },

    items () {
      return this.entries.map(entry => {entry.desc
        const Description = entry.length > this.descriptionLimit
          ? entry.desc.slice(0, this.descriptionLimit) + '...'
          : entry.desc

        return Object.assign({}, entry, { Description })
      })
    },
    
    banks () {
      return this.bankentries.map(entry => {entry.desc
        const Description = entry.desc

        return Object.assign({}, entry, { Description })
      })
    },
    
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
      console.log(this.inn)
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
      this.$http
      .post("api/lead/", JSON.stringify(this.lead), {
        headers: {
          // Overwrite Axios's automatically set Content-Type
          'Content-Type': 'application/json'
        },
        responseType: 'blob'
      })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'image.docx');
        document.body.appendChild(link);
        link.click();
        this.collapse = true
        this.collapse2 = false
        this.sended = true
      })
    },

    input_customer(){
      this.ressived = true
    },
    
    input_bank(){
      this.bank_ressived = true
    }

  },

  watch: {
    search () {
      console.log(this.search)
      // Items have already been loaded
      //if (this.items.length > 0) return

      // Items have already been requested
      if (this.isLoading) return

      this.isLoading = true

      // Lazily load input items
      this.$http.get('api/innrequest/', {params:{inn:this.search}})
        .then(res => {
          const data = res.data
          const count = data.length
          this.count = count
          this.entries = data
          console.log(res)
        })
        .finally(() => (this.isLoading = false))
    },
    banksearch() {
      console.log(this.banksearch)
      // Items have already been loaded
      //if (this.items.length > 0) return

      // Items have already been requested
      if (this.bankisLoading) return

      this.bankisLoading = true

      // Lazily load input items
      this.$http.get('api/bankrequest/', {params:{bank:this.banksearch}})
        .then(res => {
          const data = res.data
          const count = data.length
          this.bankscount = count
          this.bankentries = data
          console.log(res)
        })
        .finally(() => (this.bankisLoading = false))
    },
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