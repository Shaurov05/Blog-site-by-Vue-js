<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
      <div class="container">
            <router-link
                  :to="{ name: 'home' }"
                  class = "navber-brand"
                  >PostTime
            </router-link>

        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
                <router-link
                      :to="{ name: 'home' }"
                      class = "btn btn-sm btn-success"
                      >Home
                </router-link>
            </li>
            <li class="nav-item mx-1">
                  <router-link
                        :to="{ name: 'post-editor' }"
                        class = "btn btn-sm btn-danger"
                        >Post Blog
                  </router-link>
            </li>
            <li class="nav-item">
              <a class="btn btn-sm btn-outline-secondary" href="/accounts/logout/"
                >Logout
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

</template>

<script>
export default {
  name: "NavbarComponent"

}
</script>

<style>
  .my-navbar{
    border-bottom: 1px solid #DDD;
  }
  .navber-brand{
    font-weight: bold;
    font-size: 130%;
  }
  .navber-brand:hover {
    color: #DC3545 !important;
  }

</style>
