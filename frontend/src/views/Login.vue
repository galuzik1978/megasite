<template>
<v-app id="inspire">
    <v-main>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Зарегистрируйтесь в системе</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form @keyup.native.enter="login" ref="form">
                  <v-text-field v-model="username"
                    label="Ваше имя"
                    name="username"
                    prepend-icon="mdi-account"
                    type="text"
                    :error="error"
                    :error-messages="errorMsg"
                  ></v-text-field>

                  <v-text-field v-model="password"
                    id="password"
                    label="Пароль"
                    name="password"
                    prepend-icon="mdi-lock"
                    type="password"
                    :error="error"
                    :error-messages="errorMsg"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn @click="cancel">Отмена</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="login">Войти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
  export default {
    data(){
      return {
        username : "",
        password : "",
        error: false,
        errorCount: 1,
      }
    },
    computed: {
      errorMsg() {
        return this.error ? ['Ошибка. Попробуйте еще раз.'] : []
      },
    },
    methods: {
      login: function () {
        let username = this.username 
        let password = this.password
        this.$store.dispatch('login', { username, password})
       .then(() => {
         this.$router.push('/')
       })
       .catch(() => {
         this.$refs.form.reset()
         this.error = true
        })
      },

      cancel(){
        this.$router.go(-1)
      }
    },
    props: {
      source: String,
    },
  }
</script>