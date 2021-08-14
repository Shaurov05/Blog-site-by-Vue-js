<template>

  <div class="container mt-2">
    <h1 class="mb-2">  Post a blog </h1>
    <form @submit.prevent="onSubmit">
      <textarea
            v-model="post_body"
            rows="3"
            class="form-control"
            placeholder="What do you want to post?"
      > </textarea>
      <br>
      <button
            type="submit"
            class="btn btn-success"
       >Publish</button>
    </form>

    <p v-if="error" class="muted mt-2" > {{ error }}</p>
  </div>

</template>


<script>
import { apiService } from "@/common/api.service.js";

export default {
  name: "PostEditor",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      post_body: null,
      error: null
    }
  },

  methods :{
    onSubmit(){
      if(!this.post_body){
          this.error = "You can't send an empty post!";
      } else if (this.post_body.length > 240) {
          this.error = "Ensure this field has no more than 240 characters!";
      } else {
          let endpoint = "/api/posts/";
          let method = "POST";
          console.log(this.slug)
          if (this.slug !== undefined) {
            method = "PUT";
            endpoint += `${ this.slug }/` ;
            console.log(endpoint)
          }

          apiService(endpoint, method, { content: this.post_body })
              .then(post_data => {
                  this.$router.push({
                    name:'post',
                    params: { slug: post_data.slug }
                  })
              })
          }
        }
  },

  async beforeRouteEnter ( to, from, next ) {
    if (to.params.slug !== undefined) {
      let endpoint = `/api/posts/${ to.params.slug }/`;
      let data = await apiService(endpoint);
      return next( vm => {
        vm.post_body = data.content
      })
    } else{
      return next()
    }
  },

  created(){
    document.title = "Editor - PostTime";
  }
}

</script>

<style>
</style>
