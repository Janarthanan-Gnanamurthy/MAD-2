<template>
  <main>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <RouterLink to="/" class="navbar-brand">BookStore</RouterLink>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink to="/" class="nav-link">Home</RouterLink>
          </li>

          <li v-if="$store.state.token && $store.state.user.role === 'User'" class="nav-item">
            <RouterLink to="/mybooks" class="nav-link">My Books</RouterLink>
          </li>
          <li v-if="$store.state.token && $store.state.user.role === 'Admin'" class="d-flex">
            <RouterLink to="/admin/requests" class="nav-link">Requests</RouterLink>
            <RouterLink to="/admin/stats" class="nav-link">Stats</RouterLink>
            <RouterLink to="/admin/section/new" class="nav-link">Add Section</RouterLink>
            <RouterLink to="/admin/book/new" class="nav-link">Add Book</RouterLink>
          </li>
        </ul>

        <div class="d-flex">
          <div class="search-container">
            <input v-model="query" class="form-control me-2" type="search" placeholder="Search..." />
            <button class="btn btn-light" @click="redirectToSearch">Search</button>
          </div>

          <button v-if="$store.state.token" class="btn btn-outline-light ms-2" @click="logout">Logout ({{ $store.state.user.username }})</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <RouterView />
    </div>
  </main>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<script>
export default {
  data() {
    return {
      query: ''
    };
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logout');
      this.$router.push('/login');
    },
    redirectToSearch() {
      if (this.query.trim()) {
        this.$router.push(`/search?query=${encodeURIComponent(this.query)}`);
      }
    }
  }
};
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
}

.search-container input {
  border-radius: 20px;
}

.navbar-brand {
  font-weight: bold;
}

@media (max-width: 768px) {
  .search-container {
    margin-top: 10px;
    margin-bottom: 10px;
  }
}
</style>
