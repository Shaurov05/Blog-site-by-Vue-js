<template>
  <div class="home">
    <div class="container mt-2">
      <div v-for="post in posts"
                :key="post.pk">
          <p class="mb-0"> posted by:
            <span class="post-author"> {{ post.author }} </span>
          </p>
          <h2>
            <router-link
                  :to="{ name:'post', params: { slug: post.slug }  }"
                  class="post-link"  >
              {{ post.content }}
            </router-link>
          </h2>
          <p> Comments: {{ post.comments_count }} </p>
          <hr>
      </div>

      <div class="my-4">
        <p v-show="loadingPosts">...loading...  </p>
        <button
            v-show="next"
            @click="getPosts"
            class="btn btn-sm btn-outline-success"
        > Load More </button>
      </div>

    </div>
  </div>
</template>


<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "home",
  data () {
    return {
      posts: [],
      next: null,
      loadingPosts: false,
    }
  },
  methods: {
    getPosts() {

      let endpoint = "/api/posts/";
      if (this.next){
        endpoint = this.next;
      }
      this.loadingPosts = true

      apiService(endpoint)
        .then(data => {
          this.posts.push(...data.results)
          this.loadingPosts = false;

          if(data.next){
            this.next = data.next;
          } else {
            this.next = null;
          }
        })
    }
  },
  created(){
    this.getPosts()
    document.title = "PostTime"
    // console.log(this.posts)
  }
};
</script>


<style scoped>
.post-author{
  font-weigh: bold;
  color: #DC3545;
}

.post-link{
  font-weight: bold;
  color: black;
}

.post-link:hover {
  color: #343A40;
  text-decoration: none;
}

</style>
