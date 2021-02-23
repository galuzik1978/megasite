<template>
  <div>
    <v-card>
      <v-card-title>
        Наименование формы протокола:
      </v-card-title>
      <v-card>
        <v-card-title>
          Результаты проверки оборудования инв. №{{ data.object.reg_num }}
        </v-card-title>
        <v-divider></v-divider>
        <!-- Карта вида проверки -->
        <v-card 
          v-for="(form, index) in data.tables" 
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
          <v-card-text v-if="true">

            <!-- Главная таблица с проверяемыми параметрами -->
            <v-data-table
              :headers="form.header"
              :items="form.row"
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
              <template v-slot:expanded-item="{ header, item }">
                <td :colspan=5>
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
                    v-if="false"
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
          v-if="false"
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
          >
            Сохранить все
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-card>
  </div>
</template>

<script>
export default {
  
  props:{
    id: Number,
  },

  data: () => ({
    singleExpand: true,

    data: {
      object:{
        reg_num: 'Регистрационный номер'
      },
      tables:[
        {
          headers:{}
        }
      ]
    },
    files_table:[],
    files:[],
  }),

  computed:{

    url(){
      return "api/protocol/" + this.$attrs.wr_id + "/"
    }

  },

  watch: {
    id: {
      immediate: true,
      handler(){
        let v = this
        this.$http
        .get(this.url, {params: this.$attrs})
        .then((response) => {
          v.data = response.data
          console.log(v.data)

        })
      }
    }
  },

  methods:{

    AddDefect(){
      console.log("AddDefect")
    },

    reserve(){
      console.log('reserve')
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
  }

}
</script>

<style>

</style>