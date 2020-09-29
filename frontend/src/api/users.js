import { HTTP } from './common'

export const User = {
    list() {
        return HTTP.get('/users/')
        .then(response => {
            console.log('get_user')
            return response.data
        })
    }
}