<template>
  <v-card flat>
    <v-card-title class="text-center justify-center">
      Добавьте в форму все необходимые таблицы контроля
    </v-card-title>
    <v-card-text>

      <!-- Реестр таблиц формы -->
      <v-data-table
        hide-default-footer
        :headers="tables_header"
        :items="form.tables"
        no-data-text="Ни одна таблица не добавлена"
        class="table-extend"
        flat
        disable-pagination
      >

        <!-- Слот для нумерации выявленных несоответствий -->
        <template #item.num="{ item:value }">
          {{ (form.tables.indexOf(value) + 1) }}
        </template>

        <!-- Слот для удаления выявленных несоответствий -->
        <template #item.delete_action="{ item:value }">
          <v-icon @click="delete_table_from_form(value)">mdi-delete</v-icon>
        </template>

      </v-data-table>

      <!-- Селект для выбора таблиц формы -->
      <v-select
        v-model="form.tables"
        :items="tables"
        :menu-props="{ maxHeight: '400', maxWeight: '600' }"
        label="Добавьте таблицу"
        multiple
        hint="Выберите все необходимые для проведения контроля таблицы"
        persistent-hint
        item-text="phrasing"
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
      <v-spacer></v-spacer><v-btn color="primary">Сохранить</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data:() => ({
    tables_header: [
      {
        text: '№ п/п',
        align: 'start',
        sortable: false,
        value: 'num',
        width: '5%'
      },
      { text: 'Наименование контроля', value: 'phrasing', width: '30%' },
      { text: 'Нормативная документация, устанавливающая требования', value: 'document', width: '30%' },
      { text: '', value: 'delete_action', width: '5%' },
    ]
  }),

  props:{
    form:{},
    tables:{},
  },

}
</script>

<style>

</style>