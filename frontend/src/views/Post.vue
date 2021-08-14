<template>

<div class="single-post mt-2">
  <div v-if="post" class="container">
    <h1> {{ post.content }} </h1>
    <PostActions
        v-if="isPostAuthor"
        :slug="post.slug"
    />
    <p class="mb-0"> posted by:
      <span class="author-name"> {{ post.author }} </span>
    </p>

    <p class="mb-0">
      {{ post.created_at }}
    </p>
    <br>
    <div class="row">
      <div class="col-sm-2">
        <button
        class="btn btn-sm"
        @click="toggleUpvote"
        :class="{
          'btn-danger': userUpvotedPost,
          'btn-outline-danger': !userUpvotedPost
          }"
        ><strong v-if="userUpvotedPost">Upvoted [ {{ UpvotesCounter }} ]</strong>
        <strong v-else>Upvote [ {{ UpvotesCounter }} ]</strong>
      </button>
      </div>
      <div class="col-sm-2">
        <button
        class="btn btn-sm"
        @click="toggleDownvote"
        :class="{
          'btn-danger': userDownvotedPost,
          'btn-outline-danger': !userDownvotedPost
          }"
        ><strong v-if="userDownvotedPost">Downvoted [ {{ DownvotesCounter }} ]</strong>
        <strong v-else>Downvote [ {{ DownvotesCounter }} ]</strong>
      </button>
      </div>
    </div>
    <br>
    <hr>
    <div v-if="userHasCommented">
        <p class="comment-added"> You've already commented! </p>
    </div>
    <div v-else-if="showForm">
      <form class="card" @submit.prevent="onSubmit">
        <div class="card-header px-3">
          Comment
        </div>
        <div class="card-block">
          <textarea
            v-model="newCommentBody"
            class="form-control"
            placeholder="Share your Comment"
            rows="5"
          ></textarea>
        </div>

        <div card="card-footer px-3 mt-2">
          <br>
          <button class="btn btn-sm btn-success"
              > Submit Your Comment
          </button>
        </div>
      </form>
      <p v-if="error" class="error mt-2"> {{ error }} </p>
    </div>
    <div v-else>
      <button
          class="btn btn-sm btn-success"
          @click="showForm = true"
          > Comment

      </button>
    </div>
    <hr>
  </div>

  <div v-else>
    <h1 class="error text-center"> <br><br><br> 404 - Post Not Found </h1>
  </div>

  <div v-if="post" class="container">
      <CommentComponent
        v-for="comment in comments"
        :key="comment.id"
        :requestUser="requestUser"
        :comment="comment"
        @delete-comment="deleteComment"
      />

    <div class="my-4">
      <p v-show="loadingComments">...loading...  </p>
      <button
          v-show="next"
          @click="getPostComments"
          class="btn btn-sm btn-outline-success"
      > Load More </button>
    </div>
  </div>
</div>
</template>


<script>
import { apiService } from "@/common/api.service.js";
import CommentComponent from "@/components/Comment.vue";
import PostActions from "@/components/PostAction.vue";

export default {
  name: "Post",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },

  components: {
    CommentComponent,
    PostActions,
  },

  data(){
    return {
      post: {},
      comments: [],
      newCommentBody: null,
      error: null,
      userHasCommented: false,
      showForm: false,
      loadingComments: false,
      next: null,
      requestUser: null,

      user_has_voted: false,
      userUpvotedPost: false,
      userDownvotedPost: false,
      UpvotesCounter: 0,
      DownvotesCounter: 0,
    }
  },

  computed: {
    isPostAuthor() {
      return this.post.author === this.requestUser;
    }
  },

  methods: {
    setPageTitle(title){
      document.title = title;
    },
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    getPostData(){
      let endpoint = `/api/posts/${this.slug}/`;
      apiService(endpoint)
          .then(data => {
            if (data) {
              this.post = data;
              this.userHasCommented = data.user_has_commented;

              if (data.user_vote_type === "upvote")
              {
                this.userUpvotedPost = true;
              }
              else if (data.user_vote_type === "downvote"){
                  this.userDownvotedPost = true;
              }
              this.user_has_voted = data.user_has_voted;
              this.UpvotesCounter = data.upvotes_count;
              this.DownvotesCounter = data.downvotes_count;

              this.setPageTitle(this.post.content)
            } else {
              this.post = null;
              this.setPageTitle("404 - Page Not Found")
            }
            // console.log(data.user_vote_type)
          })
    },

    getPostComments() {
      // get a page of comments for a single Post from the REST API's paginated 'Posts Endpoint'
      let endpoint = `/api/posts/${this.slug}/comments/`;
      if (this.next){
        endpoint = this.next;
      }
      this.loadingComments = true;

      apiService(endpoint)
        .then(data => {
          this.comments.push(...data.results);
          this.loadingComments = false;

          if(data.next){
            this.next = data.next;
          } else {
            this.next = null;
          }
        })
    },
    
    toggleUpvote() {
      if (this.post.author === this.requestUser) {
        alert("cannot upvote your own post")
      } else {
        this.userUpvotedPost === false ? this.UpvotePost() : this.DeletePostVote();
      }
    },
    toggleDownvote() {
      if (this.post.author === this.requestUser) {
        alert("cannot downvote your own post")
      } else {
        this.userDownvotedPost === false ? this.DownvotePost() : this.DeletePostVote();
      }
    },
    UpvotePost() {
      this.userUpvotedPost = true;
      this.UpvotesCounter += 1;

      if (this.userDownvotedPost === true){
        this.userDownvotedPost = false;
        this.DownvotesCounter -= 1;
      }
      let endpoint = `/api/post/${ this.post.slug }/vote/`;
      apiService(endpoint, "POST", { content: "upvote" })
    },
    DownvotePost() {
      this.userDownvotedPost = true;
      this.DownvotesCounter += 1;

      if (this.userUpvotedPost === true){
        this.userUpvotedPost = false;
        this.UpvotesCounter -= 1;
      }
      let endpoint = `/api/post/${ this.post.slug }/vote/`;
      apiService(endpoint, "POST",{ content: "downvote" })
    },
    DeletePostVote() {
      this.userUpvotedPost ? this.UpvotesCounter -= 1 : null;
      this.userDownvotedPost ? this.DownvotesCounter -= 1 : null;

      this.userUpvotedPost = false;
      this.userDownvotedPost = false;
      let endpoint = `/api/post/${ this.post.slug }/vote/`;
      apiService(endpoint, "DELETE")
    },

    onSubmit() {
      // Tell the REST API to create a new comment for this post based on the user input, then update some data properties
      if (this.newCommentBody) {
        let endpoint = `/api/posts/${this.slug}/comment/`;
        apiService(endpoint, "POST", { body: this.newCommentBody })
          .then(data => {
            // The unshift() method is used to add one
            // or more elements to the beginning of an
            // array and return the length of the array.
            this.comments.unshift(data)
          })
        this.newCommentBody = null;
        this.showForm = false;
        this.userHasCommented = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "You can't send an empty comment!";
      }
    },

    async deleteComment(comment) {
      let endpoint = `/api/comments/${comment.id}/`;
      try {
        await apiService(endpoint, "DELETE")
          this.$delete(this.comments, this.comments.indexOf(comment))
          this.userHasCommented = false;
        }
      catch(err) {
        console.log(err)
      }
    }

  },

  created() {
    this.getPostData()
    this.getPostComments()
    this.setRequestUser()
    // console.log(this.posts)
  }
}

</script>


<style scoped>
.author-name{
  font-weigh: bold;
  color: #DC3545;
}
.comment-added {
  font-weight: bold;
  color: green;
}
.error {
  font-weight: bold;
  color: red;
}
</style>
