<template>
  <v-card class="mx-auto py-8" height='100%' style="position: relative">
      <v-card-title class="text-center justify-center py-6">
          Здесь могла бы быть ваша реклама
      </v-card-title>
      <v-card-text class="text-center">
        <v-btn color="primary" @click="quere">Оформить заявку на выполнение работ</v-btn>
      </v-card-text>
  </v-card>
</template>

<script>
export default {

methods:{
  quere(){
    this.$router.push("/guest/start")
  }
}

}
</script>

<style>

</style>