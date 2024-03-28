<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <main>
    <nav class="navbar bg-primary ">
      <RouterLink to="/" class="text-black">Home</RouterLink>
      <RouterLink to="/about" class="btn btn-secondary">About</RouterLink>
      <button class="btn btn-primary" @click="logout"> Log out</button>
    </nav>

    <RouterView />
  </main>
</template>

<script>
export default {
  methods:{
    async logout(){
      await this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

