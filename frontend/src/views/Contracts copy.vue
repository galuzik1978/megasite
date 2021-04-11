<template>
  <div>
      <v-card>
          <v-data-table
            :items="items"
            :headers="table.headers"
            @click:row="edit_request"
          >
          </v-data-table>
      </v-card>
  </div>
</template>

<script>
export default {
    data: ()=>({
        url: 'api/contract/',
        items: [],
        
    }),
    computed: {
      table(){
        return this.$store.state.tables['in_work_inbox']
    },
    },
    methods:{
      edit_request(event, item){
        this.$router.push({name: 'Query', params: { id: item.item.id }})
        console.log(event)
        console.log(item)
      }
    },
    mounted(){
        this.$http
        .get(this.url)
        .then((response) => {
          this.items = response.data
          console.log(this.items)
        })
    }
}
</script>

<style>

</style>