<template>
  <v-card>
    <v-card-title>
      Страница настройки прав доступа пользователей, в зависимости от их роли
    </v-card-title>
    <v-card>
      <v-card-title>
        
        <v-list dense>
          <v-subheader>Доступные роли</v-subheader>
          <v-list-item-group
            v-model="selectedrole"
            color="primary"
          >
            <v-list-item
              v-for="(item, i) in roles.items"
              :key="i"
            >
              <v-list-item-content>
                <v-list-item-title v-text='i+1 + ") " + item.name'></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action class="my-0">
                <v-btn icon @click="delete_role(i)">
                  <v-icon color="grey lighten-1">mdi-delete-circle</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list-item-group>
        </v-list>

      </v-card-title>
    </v-card>
    <v-card>
      <v-subheader>Распределение пользователей по ролям</v-subheader>
      <v-data-table
        :items="users.items"
        :headers="users.headers"
        class="elevation-1"
        :calculate-widths=true
        :loading=loading
        loading-text="Загружаем данные ... Пожалуйста, подождите"
        no-data-text="Записи таблицы не найдены."
      >
      </v-data-table>
    </v-card>
  </v-card>
</template>

<script>
export default {
  
  data:() => ({
    roles:{
      items:[
        {name:"Менеджер"},
        {name:"Администратор"},
        {name:"Директор"}
      ]
    },
    users:{
      headers:[
        {
          text: 'ID',
          value: 'id'
        },
        {
          text: 'Фамилия',
          value: 'last_name'
        },
        {
          text: 'Имя',
          value: 'first_name'
        },        
        {
          text: 'Отчество',
          value: 'profile.surname'
        },
        {
          text: 'Должность',
          value: 'profile.role.name'
        },
      ],
      items:[

      ]
    },
    loading: false,
    selectedrole: null,
    update: false,
  }),

  methods: {
    edititems(){

    },

    delete_role(i){
      console.log(this.roles.items[i].name)
    }
  },

  mounted(){
    this.$http.get('api/role/')
    .then((responce)=>{
      this.roles.items=responce.data
    })
    this.$http.get('api/user/')
    .then((responce) => {
      this.users.items = responce.data
      console.log(responce.data)
    })
    this.$http.get('api/apps/')
    .then((responce) => {
      //this.users.items = responce.data
      console.log(responce.data)
    })
  }

}
</script>

<style>

</style>