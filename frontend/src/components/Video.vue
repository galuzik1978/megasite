<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h2>Current Camera</h2>
                <div>
                    <v-file-input 
                        show-size
                        @change="previewImages($event)"
                        v-model="file"
                        accept="image/*, video/*"
                    ></v-file-input>  
                </div>
                <v-img :src="image" width="300px"></v-img>
                <pdf src="https://cdn.rawgit.com/mozilla/pdf.js/c6e8ca86/test/pdfs/freeculture.pdf"></pdf>
            </div>
        </div>
    </div>
</template>

<script>
import pdf from 'vue-pdf'
export default {
    name: "App",
    components: {
        pdf
    },
    data() {
        return {
            img: null,
            image: null,
            file: null
        };
    },
    methods:{
        previewImages(event){
            this.file = event;
            var v = this
            let reader = new FileReader()
            reader.onloadend = () => {
                v.image = reader.result;
            }
            if (event !== undefined ){
                let mime = event.type.split('/')
                switch (mime[0]) {
                    case 'image':
                        reader.readAsDataURL(event)
                        break;
                    case 'video':
                        v.image = require("@/assets/video.png")
                        break
                    case 'application':
                        if (mime[1] == 'pdf')
                            v.image = require("@/assets/pdf.png")
                        else if (mime[1] == 'vnd.openxmlformats-officedocument.wordprocessingml.document')
                            v.image = require("@/assets/word.png")
                        else if (mime[1] == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                            v.image = require("@/assets/excel.png")   
                        break
                }
            } 
            else 
                v.image = null
            
        }
    }
};
</script>