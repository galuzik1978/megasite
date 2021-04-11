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
    url: 'api/inbox/',      
  }),

  computed: {
    table(){
      return this.$store.state.tables['in_work_inbox']
    },

    items(){
      return this.$store.state.current_table
    }

  },

  methods:{

    edit_request(event, item){
      this.$router.push({name: 'Query', params: { id: item.item.id }})
      console.log(event)
      console.log(item)
    }

  },

  mounted(){
    let params = {}
    if(typeof this.table.filters == "object")
      this.table.filters.forEach(filter => {
        params[filter.field] = filter.value
      });
    this.$store.dispatch('get_current_table', {'url': this.url, 'params': params})
  }

}
</script>

<style>

</style>