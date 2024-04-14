<template>
  <div class="container mt-5">
    <h1 class="mb-4">Search Results</h1>

    <!-- Books -->
    <div v-if="results.books.length > 0" class="mt-4">
      <h3>Books</h3>
      <div class="row">
        <div v-for="book in results.books" :key="book.id" class="col-md-4 mb-4">
          <div class="card">
            <img :src="book.image_filename" class="card-img-top" alt="Book Cover" />
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text">{{ book.author }}</p>
              <!-- You can add more details here -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Sections -->
    <div v-else-if="results.sections.length > 0" class="mt-4">
      <h3>Sections</h3>
      <div class="row">
        <div v-for="section in results.sections" :key="section.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ section.name }}</h5>
              <p class="card-text">{{ section.description }}</p>
              <!-- You can add more details here -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else >
      <h3>No Matching Results</h3>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      results: {
        books: [],
        sections: []
      }
    };
  },
  async created() {
    const query = this.$route.query.query;
    if (query) {
      try {
        const response = await fetch(`http://localhost:5000/api/search?query=${query}`);
        const data = await response.json();
        this.results = data;
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    }
  },
  async beforeRouteUpdate(to, from, next) {
    const query = to.query.query;
    if (query) {
      await this.fetchData(query);
    }
    next();
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
