const DB_NAME = 'inspectionsDB'
const STORAGE_NAME = 'inspections'
const DB_VERSION = 1
let DB

export default{
    async getDB() {
        return new Promise((resolve, reject) => {
            if (DB) {
                return resolve(DB)
            }
            const request = window.indexedDB.open(DB_NAME, DB_VERSION)
            
            request.onerror = e => {
                console.log('Ошибка открытия базы', e)
                reject("Ошибка")
            }

            request.onsuccess = e => {
                DB = e.target.result
                resolve (DB)
            }

            request.onupgradeneeded = e => {
                let db = e.target.result
                db.createObjectStore(STORAGE_NAME, { 
                    autoIncrement: true, 
                    keyPath: 'id'
                })
            }
        })
    },

    async deleteProtocol(protocol) {
        const db = await this.getDB()

        return new Promise(resolve => {
            
            const transaction = db.transaction([STORAGE_NAME], 'readwrite')
            transaction.oncomplete = () => {
                resolve()
            }

            const store = transaction.objectStore(STORAGE_NAME)
            store.delete(protocol.id)
        })
    },

    async getProtocols(){
        let db = await this.getDB()

        return new Promise(resolve => {
            let transaction = db.transaction([STORAGE_NAME], 'readonly')
            transaction.oncomplete = () => {
                resolve(protocols)
            }

            const store = transaction.objectStore(STORAGE_NAME)
            const protocols = []

            store.openCursor().onsuccess = e => {
                const cursor = e.target.result
                if (cursor) {
                    protocols.push(cursor.value)
                    cursor.continue()
                }
            }
        })
    },

    async getProtocol(id){
        let db = await this.getDB()

        return new Promise(resolve => {
            let transaction = db.transaction([STORAGE_NAME], 'readonly')
            transaction.oncomplete = () => {
                resolve(protocol)
            }

            const store = transaction.objectStore(STORAGE_NAME)
            const protocol = store.get(id)

        })
    },

    async saveProtocol(protocol){
        let db = await this.getDB()

        return new Promise(resolve => {
            let transaction = db.transaction([STORAGE_NAME], 'readwrite')
            transaction.oncomplete = () => {
                resolve()
            }

            let store = transaction.objectStore(STORAGE_NAME)
            store.put({"protocol": protocol})
        })

    }
}