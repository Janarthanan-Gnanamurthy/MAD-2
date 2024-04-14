<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <main>
    <nav class="navbar bg-primary ">
      <RouterLink to="/" class="text-black">Home</RouterLink>
      <RouterLink to="/mybooks" class="btn btn-success">Mybooks</RouterLink>
      
      <!-- Search bar -->
      <div class="search-container">
        <input v-model="query" placeholder="Search..." />
        <button class="btn btn-primary" @click="redirectToSearch">Search</button>
      </div>
      
      <button class="btn btn-primary" @click="logout"> Log out</button>
    </nav>

    <RouterView />
  </main>
</template>

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
  margin-right: 10px;
}
</style>
