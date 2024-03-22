<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <main>
    <nav class="navbar bg-primary ">
      <RouterLink to="/" class="text-black">Home</RouterLink>
      <RouterLink to="/about" class="text-black">About</RouterLink>
    </nav>

    <RouterView />
  </main>
</template>


