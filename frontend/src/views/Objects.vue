<template>
  <div>
      <v-card>
          <v-data-table
            :items="items"
            :headers="table.headers"
            @dblclick:row="edit_request"
          >
          </v-data-table>
      </v-card>
  </div>
</template>

<script>
export default {
  data: ()=>({
        url: 'api/workrequest/',
        items: [],
        
  }),
  computed: {
    table(){
      return this.$store.state.tables['object']
    },
  },
  methods:{
      edit_request(event, item){
        this.$router.push({name: 'Protocol', params: { id: item.item.id, wr: item.item.wr_id}})
        console.log(event)
        console.log(item)
      }
    },
    mounted(){
      let v = this
        this.$http
        .get(this.url)
        .then((response) => {
          response.data.forEach(element => {
            let obj = element.object
            obj.wr_id = element.id
            v.items.push(element.object)
            console.log(this.items)
          });
        })
    }
}
</script>

<style>

</style>