import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Post from "../views/Post.vue";
import PostEditor from "../views/PostEditor.vue";
import CommentEditor from "../views/CommentEditor.vue";
import NotFound from "../views/NotFound.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    // with props: true, the slug parameter gets
    // passed as a prop to the component
    path: "/post/:slug",
    name: "post",
    component: Post,
    props : true
  },
  {
    // the ? sign makes the slug parameter optional. It means
    // we might send slug and if passed, the value will be passed
    // as a parameter.
    path: "/ask/:slug?",
    name: "post-editor",
    component: PostEditor,
    props: true,
  },
  {
    path: "/comment/:id",
    name: "comment-editor",
    component: CommentEditor,
    props : true
  },
  {
    path:"*",
    name: "page-not-found",
    component: NotFound,
  },

];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
