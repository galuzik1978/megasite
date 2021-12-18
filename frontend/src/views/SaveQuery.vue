<template>
  <v-card>
      <v-card-title>
          Скачайте заявку, проверьте правильность внесенных данных, распечатайте на своем фирменном бланке, подпишите, отсканируйте и отправьте нам скан
      </v-card-title>
      {{ filename }}
  </v-card>
</template>

<script>
export default {
  props:{
    filename: String
  },
}
</script>

<style>

</style>