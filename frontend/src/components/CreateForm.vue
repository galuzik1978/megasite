<template>
  <v-card flat>
    <v-card-title class="text-center justify-center">
      Выберите существующую форму
    </v-card-title>
    <v-card-text>
      <v-list dense>
        <v-subheader>Формы протоколов</v-subheader>
        <v-list-item-group
          v-model="selectedForm"
          color="primary"
          mandatory
        >
          <v-list-item
            @click="fill_form(-1)"
          >
            <v-list-item-icon>
              <v-icon>mdi-form-dropdown</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Новая пустая форма</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-for="(item, i) in form"
            :key="i"
            @click="fill_form(i)"
          >
            <v-list-item-icon>
              <v-icon>mdi-form-dropdown</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          
        </v-list-item-group>
      </v-list>
    </v-card-text>
    <v-card-title class="text-center justify-center">
      Или введите новую форму
    </v-card-title>
    <v-card-text>
      <v-text-field
        v-model="name"
        label="Имя формы"
      ></v-text-field>
    </v-card-text>
    <v-card-title class="text-center justify-center">
      Добавьте в форму все необходимые таблицы контроля
    </v-card-title>
    <v-card-text>

      <!-- Реестр таблиц формы -->
      <v-data-table
        hide-default-footer
        :headers="tables_header"
        :items="form_tables"
        no-data-text="Ни одна таблица не добавлена"
        class="table-extend"
        flat
        disable-pagination
      >

        <!-- Слот для нумерации выявленных несоответствий -->
        <template #item.num="{ item:value }">
          {{ (form_tables.indexOf(value) + 1) }}
        </template>

        <!-- Слот для удаления выявленных несоответствий -->
        <template #item.delete_action="{ item:value }">
          <v-icon @click="delete_table_from_form(form_tables.indexOf(value))">mdi-delete</v-icon>
        </template>

      </v-data-table>

      <!-- Селект для выбора таблиц формы -->
      <v-select
        v-model="form_tables"
        :items="tables"
        item-text="name"
        item-value="id"
        :menu-props="{ maxHeight: '400', maxWeight: '600' }"
        label="Добавьте таблицу"
        multiple
        hint="Выберите все необходимые для проведения контроля таблицы"
        persistent-hint
        return-object
        class="multiple_select"
      >
        <template v-slot:append-outer>
          <v-icon @click="tab=1">
            mdi-plus
          </v-icon>
        </template>
      </v-select>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer><v-btn color="primary" @click="save_form">Сохранить</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data:() => ({
    selectedForm:-1,
    name:"",
    form_tables:[],
    tables_header: [
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%'
      },
      { text: 'Наименование контроля', value: 'name', width: '30%' },
      { text: 'Нормативная документация, устанавливающая требования', value: 'document', width: '30%' },
      { text: '', value: 'delete_action', width: '5%' },
    ]
  }),

  props:{
    form:Array,
    tables:Array,
  },

  methods:{
    delete_table_from_form(value){
      console.log(value)
      this.form_tables.splice(value, 1)
    },

    save_form(){
      let data = {
        name:this.name,
        tables:this.form_tables,
      }
      if (this.selectedForm > 0){
        data['id'] = this.form[this.selectedForm-1].id
      }
      this.$http
      .post("api/form/", JSON.stringify(data), {
        headers: {
          // Overwrite Axios's automatically set Content-Type
          'Content-Type': 'application/json'
        }
      })
      .then((response) => {
        console.log(response.data)
      })
      console.log(JSON.stringify(this.form))
      console.log(this.form_tables)
    },

    fill_form(event){
      this.form_tables = []
      let tables_id
      let table
      if (event >= 0) {
        for (tables_id of this.form[event].tables){
          table = this.tables.find(table => table.id === tables_id)
          this.form_tables.push(table)
          this.selectedForm = event
          this.name = this.form[event].name
        }
      } else {
        this.name = ""
      }
      console.log(this.tables)
      console.log(table)
      console.log(this.form_tables)
    }
  },

}
</script>

<style>

</style>