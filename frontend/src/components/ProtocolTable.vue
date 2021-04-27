<template>
  <div>
    <!-- Карта вида проверки -->
    <v-card 
      v-for="(form, index) in tables" 
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
      <v-card-text v-if="!form.collapse">

        <!-- Главная таблица с проверяемыми параметрами -->
        <v-data-table
          :headers="form.header"
          :items="form.dataset"
          :single-expand=true
          :expanded.sync="form.expanded"
          item-key="num"
          show-expand
          class="elevation-1"
          hide-default-footer
          disable-pagination
        >
          <!-- Слот выбора результатов контроля -->
          <template v-slot:item.customize="{ item, header }">
            <v-select
              v-model="item[header.data]"
              v-if="header.type==3"
              :items="header.selectchoices"
            ></v-select>
            <v-text-field
              v-model="item[header.data]"
              v-else
            ></v-text-field>
          </template>

          <!-- Слот раскрывающейся строки для отображения выявленных несоответствий -->
          <template v-slot:expanded-item="{ header, item }">
            <td :colspan=form.header.length>
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
                  <v-icon @click="delete_defect(item.defects, value)">mdi-delete</v-icon>
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
                class="multiple_select hide_select"
              >
                <template v-slot:append-outer>
                  <v-icon @click="AddDefect">
                    mdi-plus
                  </v-icon>
                </template>
              </v-select>
              
              <!-- Таблица с приложениями к выявленным замечаниям -->
              <v-data-table
                :headers="data.annex_table_headers"
                :items="item.annex_table"
                hide-default-header
                hide-default-footer
                v-if="item.annex_table.length>0"
                class="table-extend my-4"
              >

                <template #item.num="{ item:val }">
                  {{ item.annex_table.indexOf(val) + 1 }}
                </template>

                <template #item.actions="{ item:val }">
                  <v-icon @click="delete_file(item.annex_table, val)">mdi-delete</v-icon>
                </template>

                <!-- Слот для вставки изображений в таблицу приложений -->
                <template #item.img="{ item }">
                  <v-img :src="images[item.img]" width="150px"></v-img>
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
                  @change="file_append(item.annex_table)"
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
              </v-card-actions>
            </td>
          </template>
        </v-data-table>



        <!-- Таблица с общими приложениями к таблице -->
        <v-data-table
          :headers="data.annex_table_headers"
          :items="form.annex_table"
          hide-default-header
          hide-default-footer
          v-if="form.annex_table.length>0"
          class="my-4"
        >

          <template #item.num="{ item }">
            {{ form.annex_table.indexOf(item) + 1 }}
          </template>

          <template #item.actions="{ item }">
            <v-icon @click="delete_file(form.annex_table, item)">mdi-delete</v-icon>
          </template>

          <!-- Слот для вставки изображений в таблицу приложений -->
          <template #item.img="{ item }">
            <v-img :src="images[item.img]" width="150px"></v-img>
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
            @change="file_append(form.annex_table)"
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
            Сохранить таблицу
          </v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>

export default {
  
  props:{
    tables: Array,
    images: Array,
    annex_table: Array,
    data: Object
  },

  data: () => ({
    files: [],
  }),

  methods:{

    delete_defect(table, value){
      let editedIndex = table.indexOf(value)
      table.splice(editedIndex, 1)
    },

    file_append(files_table){            
      let reader = new FileReader()
      let new_file = {
        img: "",
        filename: this.files[0].name,
        filesize: this.files[0].size/1000 + ' Kb',
      }
      reader.onloadend = () => {
          new_file.img = this.images.push(reader.result)-1;
          
      }
      if (this.files[0] !== undefined ){
        let mime = this.files[0].type.split('/')
        switch (mime[0]) {
          case 'image':
            reader.readAsDataURL(this.files[0])
            break;
          case 'video':
            new_file.img = this.images.push(require("@/assets/video.png"))-1
            break
          case 'audio':
            new_file.img = this.images.push(require("@/assets/audio.png"))-1
            break
          case 'application':
            if (mime[1] == 'pdf')
              new_file.img = this.images.push(require("@/assets/pdf.png"))-1
            else if (mime[1] == 'vnd.openxmlformats-officedocument.wordprocessingml.document')
              new_file.img = this.images.push(require("@/assets/word.png"))-1
            else if (mime[1] == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
              new_file.img = this.images.push(require("@/assets/excel.png"))-1 
            break
        }
        this.annex_table.push({file:this.files[0], img:this.images.length})
      } 
      else 
        new_file.img = null

      files_table.push(new_file)
      
      this.files.pop()
    },

    delete_file(files, item){
      let editedIndex = files.indexOf(item)
      files.splice(editedIndex, 1)
      this.annex_table.splice(editedIndex, 1)
    },

    AddDefect(){
      console.log("AddDefect")
    },

  },

}
</script>

<style>

</style>