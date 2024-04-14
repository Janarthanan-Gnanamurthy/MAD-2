<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <main>
    <nav class="navbar bg-primary ">
      <RouterLink to="/" class="text-black">Home</RouterLink>

      <RouterLink v-if='$store.state.user.role == "User"' to="/mybooks" class="btn btn-success">Mybooks</RouterLink>
      
      <div v-if="$store.state.token" class="d-flex">
        <div class="search-container">
          <input v-model="query" placeholder="Search..." />
          <button class="btn btn-primary" @click="redirectToSearch">Search</button>
        </div>
        
        <button class="btn btn-primary" @click="logout">{{ $store.state.user.username }}</button>
      </div>
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
