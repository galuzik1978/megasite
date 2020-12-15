<template>
<div>
  <v-form>
    <v-text-field
      label="Наименование формы"
      v-model=form_data.form_name
    >  
    </v-text-field>
    <v-card
      v-for="(form, index) in form_data.headers" 
      :key="form.id"
    >
      <v-toolbar dense>
        <v-text-field
          label="Наименование раздела"
          v-model=form.name           
          full-width
          dense
        > 
          <template v-slot:prepend>
            {{ index +1 }}
          </template>
        </v-text-field> 
      </v-toolbar> 
      <v-card-text>
        <v-data-table
          :headers="header"
          :items="form.header"
          hide-default-footer
          disable-pagination
        >

          <template v-slot:item.align={item}>
            <v-select
              :items="alignment"
              v-model=item.align
            ></v-select>
          </template>
          
          <template v-slot:item.sortable={item}>
            <v-checkbox
              v-model=item.sortable
            ></v-checkbox>
          </template>

          <template v-slot:item.text={item}>
            <v-text-field
              v-model=item.text
            ></v-text-field>
          </template>
          
          <template v-slot:item.value={item}>
            <v-text-field
              v-model=item.value
            ></v-text-field>
          </template>

          <template v-slot:item.width={item}>
            <v-text-field
              v-model=item.width
            ></v-text-field>
          </template>
          
          <template v-slot:item.delete={item}>
            <v-icon @click="delete_row(form.header, item)">
              mdi-delete
            </v-icon>
          </template>
          
          <template v-slot:top>
            <v-card-title>
              Формат контролируемых параметров
            </v-card-title>
          </template>
        </v-data-table>
        <v-btn @click="add_row(form.header)">Добавить строку</v-btn>
      </v-card-text> 
    </v-card>
    <v-btn @click="add_part">Добавить раздел</v-btn>
  </v-form>


  <v-card>
    <v-card-title>
      Результаты проверки оборудования инв. №{{inv}}
    </v-card-title>
    <v-divider></v-divider>
    <!-- Карта вида проверки -->
    <v-card 
      v-for="(form, index) in form_data.headers" 
      :key="form.id"
    >
      <v-app-bar
        flat
      >
        <v-app-bar-nav-icon @click="form.collapse = !form.collapse"></v-app-bar-nav-icon>

        <v-toolbar-title>
          {{ form.name }}
        </v-toolbar-title>
      </v-app-bar>
      <v-card-text v-if="form.collapse">

        <!-- Главная таблица с проверяемыми параметрами -->
        <v-data-table
          
          :headers="form.header"
          :items="form.dataset"
          :single-expand="singleExpand"
          :expanded.sync="form.expanded"
          item-key="num"
          show-expand
          class="elevation-1"
          hide-default-footer
          disable-pagination
        >
          <!-- Слот номерации строк главной таблицы -->
          

          <!-- Слот выбора результатов контроля -->
          <template v-slot:item.result="{ item }">
            <v-select
              :items="form.results"
              :label="item.result"
            ></v-select>
          </template>

          <!-- Слоты для ввода результатов измерения сопротивления изоляции -->
          <template v-slot:item.AB>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.AC>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.BC>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.AN>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.BN>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.CN>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.APE>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.BPE>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.CPE>
            <v-text-field ></v-text-field>
          </template>

          <template v-slot:item.NPE>
            <v-text-field ></v-text-field>
          </template>
          
          <template v-slot:item.resistant>
            <v-text-field ></v-text-field>
          </template>

          <!-- Слот раскрывающейся строки для отображения выявленных несоответствий -->
          <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length">
              <v-card-title class="text-center" style="display:block;">
                Выявленные дефекты
              </v-card-title>

              <!-- Вложенная таблица выявленных несоответствий -->
              <v-data-table
                hide-default-footer
                :headers="form.defects_header"
                :items="item.defects"
                no-data-text="Несоответствия не зафиксированы"
                class="table-extend"
                flat
                disable-pagination
              >

                <!-- Слот для нумерации выявленных несоответствий -->
                <template #item.num="{ item:value }">
                  {{ index + 1 + "." + (item.defects.indexOf(value) + 1) }}
                </template>

                <!-- Слот для удаления выявленных несоответствий -->
                <template #item.delete_action="{ item:value }">
                  <v-icon @click="delete_defect(item.files_table, value)">mdi-delete</v-icon>
                </template>

              </v-data-table>

              <!-- Селект для заполнения выявленных несоответствий -->
              <v-select
                v-model="item.defects"
                :items="form.defects"
                :menu-props="{ maxHeight: '400', maxWeight: '600' }"
                label="Добавьте выявленное несоответствие"
                multiple
                hint="Выберите все обнаруженные насоответствия"
                persistent-hint
                item-text="phrasing"
                return-object
                class="multiple_select"
              >
                <template v-slot:append-outer>
                  <v-icon @click="AddDefect">
                    mdi-plus
                  </v-icon>
                </template>
              </v-select>
              
              <!-- Таблица с приложениями к выявленным замечаниям -->
              <v-data-table
                :headers="form_data.files_table_headers"
                :items="item.files_table"
                hide-default-header
                hide-default-footer
                v-if="item.files_table.length>0"
              >

                <template #item.num="{ item:val }">
                  {{ item.files_table.indexOf(val) + 1 }}
                </template>

                <template #item.actions="{ item:val }">
                  <v-icon @click="delete_file(item.files_table, val)">mdi-delete</v-icon>
                </template>

                <!-- Слот для вставки изображений в таблицу приложений -->
                <template #item.img="{ item }">
                  <v-img :src="item.img" width="150px"></v-img>
                </template>

              </v-data-table>
              <!-- Приложение файлов в форме -->
              <v-card-actions>
                <v-file-input
                  v-model="files"
                  placeholder="Загрузите дополнительные файлы"
                  label="Выберите файл"
                  multiple
                  prepend-icon="mdi-paperclip"
                  @change="file_append(item.files_table)"
                  accept="image/*, video/*, audio/*"
                >
                  <template v-slot:selection="{ text }">
                    <v-chip
                      small
                      label
                      color="primary"
                    >
                      {{ text }}
                    </v-chip>
                  </template>
                </v-file-input>
                <v-spacer></v-spacer>
                <v-btn
                  @click="reserve"
                >
                  Сохранить все
                </v-btn>
              </v-card-actions>
            </td>
          </template>
        </v-data-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            @click="reserve"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>

    <!-- Таблица с общими приложениями к форме -->
    <v-data-table
      :headers="form_data.files_table_headers"
      :items="files_table"
      hide-default-header
      hide-default-footer
      v-if="files_table.length>0"
    >

      <template #item.num="{ item }">
        {{ files_table.indexOf(item) + 1 }}
      </template>

      <template #item.actions="{ item }">
        <v-icon @click="delete_file(files_table, item)">mdi-delete</v-icon>
      </template>

      <!-- Слот для вставки изображений в таблицу приложений -->
      <template #item.img="{ item }">
        <v-img :src="item.img" width="150px"></v-img>
      </template>

    </v-data-table>

    <!-- Приложение файлов в форме -->
    <v-card-actions>
      <v-file-input
        v-model="files"
        placeholder="Загрузите дополнительные файлы"
        label="Выберите файл"
        multiple
        prepend-icon="mdi-paperclip"
        @change="file_append(files_table)"
        accept="image/*, video/*, audio/*"
      >
        <template v-slot:selection="{ text }">
          <v-chip
            small
            label
            color="primary"
          >
            {{ text }}
          </v-chip>
        </template>
      </v-file-input>
      <v-spacer></v-spacer>
      <v-btn
        @click="saveProtocol"
      >
        Сохранить все
      </v-btn>
    </v-card-actions>
  </v-card>
</div>
</template>

<script>
export default {
  data:() => ({
        protocol: null,
        inv: "1234-AS-12",
        collapse1: true,
        singleExpand: true,
        files:[],
        files_table:[],
        alignment:[
          'start', 'center', 'end'
        ],
        header:[
          {
            text: 'Текст',
            align: 'start',
            sortable: true,
            value: 'text',
          },
          {
            text: 'Выравнивание',
            align: 'start',
            sortable: false,
            value: 'align',
            width: '10%'
          },
          {
            text: 'Сортировка',
            align: 'start',
            sortable: false,
            value: 'sortable',
            width: '5%'
          },
          {
            text: 'Значение',
            align: 'start',
            sortable: true,
            value: 'value',
            width: '15%'
          },
          {
            text: 'Ширина',
            align: 'start',
            sortable: false,
            value: 'width',
            width: '5%'
          },
          {
            text: '',
            align: 'start',
            sortable: false,
            value: 'delete',
            width: '5%'
          },
        ],
        headers_template:{
          name:"",
          id:"",
          expanded:[],
          collapse:false,
          header:[],
          dataset:[],
          defects_header:[],
          defects:[],
        },
        form_data:{
          form_name:"",
          files_table_headers:[ 
            {
              text: "№ п/п",
              value: 'num',
              width: '5%',
            },
            {
              text: "Изображение",
              value: 'img',
              width: '30%',
            },
            {
              text: "Имя файла",
              value: 'filename',
              width: '30%',
            },
            {
              text: "Размер файла",
              value: 'filesize',
              width: '20%',
            },
            {
              text: "Удалить",
              value: 'actions',
              width: '15%',
            },
          ],
          headers: [
            {
              name: "Визуальный контроль",
              id: "1",
              expanded: [],
              collapse: false,
              header:[
                {
                  text: '№ п/п',
                  align: 'start',
                  sortable: true,
                  value: 'num',
                  width: '5%'
                },
                { text: 'Наименование составных элементов электрооборудования лифта', value: 'element', width: '35%' },
                { text: 'Нормативная документация и перечень пунктов, устаналвивающих требования', value: 'document', width: '35%' },
                { text: 'Результаты контроля', value: 'result', width: '20%' },
                { text: '', value: 'data-table-expand', width: '5%' },
              ],
              dataset: [
                {
                  num: '1',
                  element: 'Аппараты защиты',
                  document: 'ГОСТ Р 53780 п.5.5.1.16; ГОСТ Р 53783 п.В.3.1.4;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
                {
                  num: '2',
                  element: 'Электропроводка',
                  document: 'ГОСТ Р 53780 п.5.5.1.1; 5.5.1.2; 5.5.1.4-5.5.1.6; 5.5.1.9-5.5.1.10; ГОСТ Р 53783 п.В.3.1.4;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
                {
                  num: '3',
                  element: 'Электрооборудование',
                  document: 'ГОСТ Р 53780 п.5.5.1.1-5.5.1.13;5.5.1.15; ГОСТ Р 53783 п.В.3.1.4;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
                {
                  num: '4',
                  element: 'Освещение и электроустановочные устройства',
                  document: 'ГОСТ Р 53780 п. 5.5.6.1-5.5.6.4;5.5.6.6-5.5.6.15;  ГОСТ Р 53783 п.В.3.1.4;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
                {
                  num: '5',
                  element: 'Заземление (зануление)',
                  document: 'ГОСТ Р 53780 п.5.5.5.7-5.5.5.8;5.5.1.13-5.5.1.14; ГОСТ Р 53783 п.В.3.1.4;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
                {
                  num: '6',
                  element: 'Маркировка элементов электрооборудования',
                  document: 'ГОСТ Р 53780 п.5.5.1.15;5.5.5.2;5.5.5.3;',
                  result: null,
                  defects:[],
                  files_table:[],
                },
              ],
              results: ['Не произведен', 'Соответствует', 'Не соответствует', 'Не подлежит контролю'],
              defects_header:[
                {
                  text: '№ п/п',
                  align: 'start',
                  sortable: false,
                  value: 'num',
                  width: '5%'
                },
                { text: 'Наименование составных элементов электрооборудования лифта', value: 'phrasing', width: '30%' },
                { text: 'Нормативная документация и перечень пунктов, устанавливающих требования', value: 'document', width: '30%' },
                { text: '', value: 'delete_action', width: '5%' },
              ],
              defects: [
                { 
                  phrasing: "наличие освещения этажных площадок перед дверями шахты лифта;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "наличие правил пользования лифтом и табличек с номерами телефонов для экстренной связи;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "состояние ограждения шахты на предмет отсутствия повреждений;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "состояние порогов и обрамлений проемов дверей шахты и кабины;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "состояние ограждения дверей шахты и кабины на предмет отсутствия повреждений, коррозии;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "состояние раздвижных решетчатых дверей кабины на грузовых лифтах, оборудованных такими дверями, а также измеряют просвет между полосами закрытой двери;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "зазоры между сомкнутыми створками автоматических раздвижных дверей шахты и кабины в местах притвора, между створками и порогами порталов, а также между лицевыми поверхностями створок и обвязками дверного проема;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "наличие перекрытия створками автоматических раздвижных дверей шахты и кабины обвязки дверного проема;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "наличие информации о нахождении кабины на этаже для лифтов, оборудованных распашными дверями шахты;",
                  document: "ГОСТ Р 53782-2010"
                },
                {
                  phrasing: "крепление постов управления в кабине и на этажах, а также состояние постов управления на предмет отсутствия повреждений постов управления и кнопок;",
                  document: "ГОСТ Р 53782-2010"
                }
              ],
            },
            {
              name: "Испытания сопротивления изоляции",
              id: "2",
              expanded: [],
              collapse: false,
              header:[
                {
                  text: '№ п/п',
                  align: 'start',
                  sortable: false,
                  value: 'num',
                  width: '5%'
                },
                { 
                  text: 'Наименование линий, электричских машин по проекту', 
                  value: 'element', 
                  width: '15%' 
                },
                {
                  text: 'Рабочее напряжение',
                  value: 'voltage',
                  width: '5%'
                },
                {
                  text: 'Кол-во жил',
                  value: 'wires',
                  width: '5%'
                },
                {
                  text: 'Сечение',
                  value: 'diam',
                  width: '5%'
                },
                {
                  text: 'Напряжение мегаомметра, В',
                  value: 'control_voltage',
                  width: '5%'
                },
                {
                  text: 'Допустимое сопротивление изоляции, МОм',
                  value: 'acceptable_resistance',
                  width: '5%'
                },
                {
                  text: 'A-B',
                  value: 'AB',
                  width: '5%'
                },
                {
                  text: 'B-C',
                  value: 'BC',
                  width: '5%'
                },
                {
                  text: 'A-C',
                  value: 'AC',
                  width: '5%'
                },
                {
                  text: 'A-N',
                  value: 'AN',
                  width: '5%'
                },
                {
                  text: 'B-N',
                  value: 'BN',
                  width: '5%'
                },
                {
                  text: 'C-N',
                  value: 'CN',
                  width: '5%'
                },
                {
                  text: 'A-PE',
                  value: 'APE',
                  width: '5%'
                },
                {
                  text: 'B-PE',
                  value: 'BPE',
                  width: '5%'
                },
                {
                  text: 'C-PE',
                  value: 'CPE',
                  width: '5%'
                },
                {
                  text: 'N-PE',
                  value: 'NPE',
                  width: '5%'
                },
                { text: '', value: 'data-table-expand', width: '5%' },
              ],
              dataset:[
                {
                  num: '1',
                  element: 'От ВУ до 1ВА',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '2',
                  element: 'От КВ  и КБ до обмотки (Б)',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                }, 
                {
                  num: '3',
                  element: 'От КМ и КН до обмотки (М)М1',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                }, 
                {
                  num: '4',
                  element: 'От КН  и КВ до ЭмТ',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '5',
                  element: 'Обмотка Б скорости М1',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '6',
                  element: 'Обмотка М скорости М1',
                  voltage: '380В',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '7',
                  element: 'Обмотка Эм  Т',
                  voltage: '220в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '8',
                  element: 'От РОД и РЗД до Эл.дв.М2',
                  voltage: '95в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '9',
                  element: 'Обмотка эл.двигателя М2',
                  voltage: '95в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '10',
                  element: 'От ВАЗ (ПР1) до ТР1',
                  voltage: '380в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '11',
                  element: 'От ТР1 до ВП3',
                  voltage: '85в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '12',
                  element: 'Обмотка ТР1 первичная',
                  voltage: '380в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '13',
                  element: 'Обмотка ТР1 вторичная',
                  voltage: '95в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '14',
                  element: 'Обмотка ТР1 вторичная',
                  voltage: '85в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '15',
                  element: 'Цепь управления',
                  voltage: '110в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '16',
                  element: 'От ПР2 до ТР3',
                  voltage: '380в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '17',
                  element: 'Обмотка Тр3 первичная',
                  voltage: '380в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '18',
                  element: 'Обмотка Тр3 вторичная',
                  voltage: '24в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '19',
                  element: 'Цепи сигнализации',
                  voltage: '24в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
                {
                  num: '20',
                  element: 'Цепи освещения шахты',
                  voltage: '220в',
                  wires: '4',
                  diam: '4',
                  control_voltage: '1000',
                  acceptable_resistance: '1',
                  files_table:[],
                },
              ]
            },
            {
              name: "Данные измерительного контроля наличия цепи между заземленным электрооборудованием и элементами заземления лифта.",
              id: "3",
              expanded: [],
              collapse: false,
              header:[
                {
                  text: '№ п/п',
                  align: 'start',
                  sortable: false,
                  value: 'num',
                  width: '5%'
                },
                { 
                  text: 'Местоположение и наименование электрооборудования', 
                  value: 'element', 
                  width: '65%' 
                },
                {
                  text: 'Количество проверенных элементов',
                  value: 'quantity',
                  width: '15%'
                },
                {
                  text: 'R перех измеренное, Ом',
                  value: 'resistant',
                  width: '15%'
                },
                { text: '', value: 'data-table-expand', width: '5%' },
              ],
              dataset:[
                {
                  num:'1',
                  element:' Жила N и PE вводного силового кабеля и магистраль зануления (контур)',
                  quantity:'1',
                  files_table:[],
                },
                {
                  num:'2',
                  element:' Корпус ВУ и контур',
                  quantity:'1',
                  files_table:[],
                },
                {
                  num:'3',
                  element:' Контур от ВУ до НКУ',
                  quantity:'1',
                  files_table:[],
                },
                {
                  num:'4',
                  element:' Каркас панели или шкафа НКУ и контур 1шт.',
                  quantity:'1',
                  files_table:[],
                }

              ]
            }
          ],
        }
    }),

  computed: {
    newId: function(){
      return this.form_data.headers.length+1

    }
  },

  methods:{

    deepClone(obj) {
      let clObj;
      if (Object.prototype.toString.call(obj) == "[object Array]"){
        clObj = []
      } else {
        clObj = {}
      }
      for(const i in obj) {
        if (obj[i] instanceof Object) {
          clObj[i] = this.deepClone(obj[i]);
          continue;
        }
        clObj[i] = obj[i];
      }
      return clObj;
    },
    
    delete_defect(form, item){
      let editedIndex = form.defects.indexOf(item)
      form.defects.splice(editedIndex, 1)
    },

    delete_row(form, item){
      let editedIndex = form.indexOf(item)
      form.splice(editedIndex, 1)
    },

    delete_file(files, item){
      let editedIndex = files.indexOf(item)
      files.splice(editedIndex, 1)
    },

    AddDefect(){
      console.log("AddDefect")
    },

    add_part(){
      let tmp = this.deepClone(this.headers_template)
      tmp.id = this.newId
      this.form_data.headers.push(tmp)
    },
    
    add_row(table){
      table.push({})
    },

    file_append(files_table){            
      let reader = new FileReader()
      let new_file = {
        img: "",
        filename: this.files[0].name,
        filesize: this.files[0].size/1000 + ' Kb'
      }
      reader.onloadend = () => {
          new_file.img = reader.result;
      }
      if (this.files[0] !== undefined ){
        let mime = this.files[0].type.split('/')
        switch (mime[0]) {
          case 'image':
            reader.readAsDataURL(this.files[0])
            break;
          case 'video':
            new_file.img = require("@/assets/video.png")
            break
          case 'audio':
            new_file.img = require("@/assets/audio.png")
            break
          case 'application':
            if (mime[1] == 'pdf')
              new_file.img = require("@/assets/pdf.png")
            else if (mime[1] == 'vnd.openxmlformats-officedocument.wordprocessingml.document')
              new_file.img = require("@/assets/word.png")
            else if (mime[1] == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
              new_file.img = require("@/assets/excel.png")   
            break
        }
      } 
      else 
          new_file.img = null
      
      files_table.push(new_file)
      this.files.pop()
    },

    reserve(){
      console.log('reserve')
    },
    
    async deleteProtocol(protocol) {
      console.log('delete', protocol.id);
      await this.$store.dispatch('deleteProtocol', protocol);
      this.$store.dispatch('getProtocols');
    },

    async saveProtocol() {
      await this.$store.dispatch('addProtocol', "1223");
      console.log('back');
    }

  },

  created() {
    this.$store.dispatch('getProtocols');
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

</style>