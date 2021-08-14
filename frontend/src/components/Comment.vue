<template>
  <div class="single-comment">
    <p class="text-muted">
      <strong>{{ comment.author }}</strong> &#8901; {{ comment.created_at }}
    </p>
    <p>{{ comment.body }}</p>
    <div v-if="isCommentAuthor">
      <router-link
        :to="{ name: 'comment-editor', params: { id: comment.id } }"
        class="btn btn-sm btn-outline-secondary mr-1"
        >Edit
      </router-link>
      <button
        class="btn btn-sm btn-outline-danger"
        @click="triggerDeleteComment"
        >Delete
      </button>
    </div>
    <div v-else>
      <button
        class="btn btn-sm"
        @click="toggleLike"
        :class="{
          'btn-danger': userLikedComment,
          'btn-outline-danger': !userLikedComment
          }"
        ><strong v-if="userLikedComment">Liked [{{ likesCounter }}]</strong>
        <strong v-else>Like [{{ likesCounter }}]</strong>
      </button>
    </div>
    <hr>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "CommentComponent",
  props: {
    comment: {
      type: Object,
      required: true
    },
    requestUser: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      userLikedComment: this.comment.user_has_voted,
      likesCounter: this.comment.likes_count,
    }
  },
  computed: {
    isCommentAuthor() {
      // return true if the logged in user is also the author of the Comment instance
      return this.comment.author === this.requestUser;
    }
  },
  methods: {
    toggleLike() {
      this.userLikedComment === false
        ? this.likeComment()
        : this.unLikeComment()
    },
    likeComment() {
      this.userLikedComment = true;
      this.likesCounter += 1;
      let endpoint = `/api/comments/${ this.comment.id }/like/`;
      apiService(endpoint, "POST")
    },
    unLikeComment() {
      this.userLikedComment = false;
      this.likesCounter -= 1;
      let endpoint = `/api/comments/${ this.comment.id }/like/`;
      apiService(endpoint, "DELETE")
    },
    triggerDeleteComment() {
      // emit an event to delete an Comment instance
      this.$emit("delete-comment", this.comment)
    }
  }
}
</script>
