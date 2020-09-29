<template>
  <div>
    <main_screen 
    :items="items"
    v-if="loading"
    ></main_screen>
  </div>
</template>

<script>
import main_screen from '../components/mian_screen'
  export default {
    components:{
      main_screen
    },
    props: {
      
    },
    data: () => ({
    
    table_url: 'api/inbox/',
    table_name: '',
    content: {
      title: 'Добавить контакт',
      fields: [
        {
          type: 'text',
          text: 'Имя',
          width: 12,
          icon: 'fa fa-user',
          value: ""
        },
        {
          type: 'text',
          text: 'Компания',
          width: 6,
          icon: 'mdi-mail',
          value: ""
        },
        {
          type: 'text',
          text: 'Должность',
          width: 6,
          value: ""
        },
        {
          type: 'email',
          text: 'E-mail',
          width: 6,
          icon: 'mdi-mail',
          value: ""
        },
        {
          type: 'text',
          text: 'Телефон',
          width: 6,
          icon: 'mdi-phone',
          value: ""
        },
        {
          type: 'text',
          text: 'Город',
          width: 6,
          icon: 'mdi-phone',
          value: "Лондон"
        },
      ]
    },
    menus: this,
    headers: [
      {
        text: 'Номер',
        align: 'center',
        sortable: true,
        value: 'num',
      },
      { text: 'Дата', value: 'date' },
      { text: 'Отправитель', value: 'sender.first_name' },
      { text: 'Тема', value: 'title' },
      { text: 'Содержание', value: 'content' },
      { text: 'Приложение', value: 'annex' },
      { text: 'Статус', value: 'send_status.name' },
      { text: 'Тип работы', value: 'type_work.name' },
      { text: 'Действия', value: 'actions', sortable: false }
    ],
    edit: {
      title: 'Добавить контакт',
      fields:[
        {
          type: 'text',
          text: 'Номер',
          width: 6,
          icon: 'fa fa-hashtag',
          name: "num",
          value: ""
        },
        {
          type: 'date',
          text: 'Дата',
          width: 6,
          icon: 'mdi-calendar',
          name: "num",
          value: ""
        },
        {
          type: 'text',
          text: 'Отправитель',
          width: 6,
          icon: 'fa fa-user',
          name: "num",
          value: "",
          url: '/api/sender/',
          subname: 'last_name + first_name'
        },
        {
          type: 'text',
          text: 'Тема',
          width: 12,
          icon: 'mdi-tag-text-outline',
          name: "title",
          value: ""
        },
        {
          type: 'textarea',
          text: 'Содержание',
          width: 12,
          icon: 'mdi-clipboard-text',
          name: "content",
          value: ""
        },
        {
          type: 'file',
          text: 'Приложение',
          width: 12,
          name: "annex"
        },
        {
          type: 'select',
          text: 'Статус',
          width: 6,
          icon: 'mdi-flag-checkered',
          name: "send_status",
          value: "",
          url: '/api/send_status/',
          subname: 'name'
        },
        {
          type: 'text',
          text: 'Тип работы',
          width: 6,
          icon: 'mdi-clipboard-check',
          name: "type_work",
          value: "",
          url: '/api/type_work/',
          subname: 'name'
        }
      ],
    },
  }),
  computed: {

    title() {
      return this.$store.state.title
    },

    items() {
      return this.$store.state.desktop
    },
    
    loading() {
      return this.$store.state.status == 'loading' ? false : true
    }
  },
  beforeMount() { document.title = this.title },
  beforeUpdate() { document.title = this.title }
}
</script>