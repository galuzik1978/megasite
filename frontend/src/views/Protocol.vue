<template>
  <div>
    <v-card>
      <v-card-title>
        Наименование формы протокола: «{{data.object.form.name}}»
      </v-card-title>
      <v-card>
        <v-card-title>
          Результаты проверки оборудования инв. №{{ data.object.reg_num }}
        </v-card-title>
        <v-divider></v-divider>
        <protocolTable
          :tables=data.tables
          :annex_table=annex_table
          :images=images
          :data=data
        ></protocolTable>

        <!-- Таблица с общими приложениями к форме -->
        <v-data-table
          :headers="data.annex_table_headers"
          :items="data.annex_table"
          hide-default-header
          hide-default-footer
          v-if="data.annex_table.length>0"
          class="my-4"
        >

          <template #item.num="{ item }">
            {{ data.annex_table.indexOf(item) + 1 }}
          </template>

          <template #item.actions="{ item }">
            <v-icon @click="delete_file(data.annex_table, item)">mdi-delete</v-icon>
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
            @change="file_append(data.annex_table)"
            accept="image/*, video/*, audio/*"
            ref="file"
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
            @click="save_all"
          >
            Сохранить все
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-card>
  </div>
</template>

<script>
import protocolTable from "../components/ProtocolTable";
export default {
  
  props:{
    id: Number,
  },

  components:{
    protocolTable
  },

  data: () => ({
    singleExpand: true,

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
          collapse:true
        }
      ],
      annex_table:[],
    },

    files_table:[],
    files:[],
    file:'',
    images:[],
    annex_table:[]
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
          //Считываем изображения для файлов, полученных с сервера
          v.data.annex_table.forEach( url => {
            url.img = this.images.push(this.$http.defaults.baseURL + url.file) - 1
          })
          v.data.tables.forEach( t => {
            t.annex_table.forEach( url => {
              url.img = this.images.push(this.$http.defaults.baseURL + url.file) - 1
            })
            t.dataset.forEach( r => {
              r.annex_table.forEach( url =>{
                url.img = this.images.push(this.$http.defaults.baseURL + url.file) - 1
              })
            })
          })
        })
      }
    }
  },

  methods:{
    collapse(item){
      console.log(item)
    },

    AddDefect(){
      console.log("AddDefect")
    },

    delete_defect(table, value){
      let editedIndex = table.indexOf(value)
      table.splice(editedIndex, 1)
    },

    reserve(){
      console.log('reserve')
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

    save_all(){
      let formData = new FormData()
      formData.append('params', JSON.stringify(this.$attrs))
      formData.append('data', JSON.stringify(this.data))
      this.annex_table.forEach( elem => {
        formData.append('file_'+elem.img, elem.file)
      });
      this.$http
      .put(this.url, formData,
        {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
        })
      .then((response) => {
        console.log(response)
      })
    },

  },

}
</script>

<style>

  .multiple_select.hide_select .v-select__selections{
    display:none;
  }

  .v-data-table__expanded.v-data-table__expanded__content{
    background-color: gainsboro;
  }

  .theme--light.v-data-table.table-extend{
    background-color: gainsboro;
  }

</style>