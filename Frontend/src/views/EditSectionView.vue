<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Edit Section</h1>
    
    <form @submit.prevent="updateSection" class="col-md-6 offset-md-3">
      <div class="form-group">
        <label for="name">Section Name:</label>
        <input type="text" class="form-control" id="name" v-model="section.name" required>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea class="form-control" id="description" v-model="section.description" rows="3"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Update Section</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      section: {
        id: null,
        name: '',
        description: ''
      }
    };
  },
  mounted() {
    // Fetch section data by ID from the backend
    const sectionId = this.$route.params.section_id;
    fetch(`http://localhost:5000/sections/${sectionId}`, {
      headers: {
        'Authorization': `Bearer ${this.$store.state.token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      this.section = data;
    });
  },
  methods: {
    updateSection() {
      const sectionId = this.$route.params.section_id;
      
      fetch(`http://localhost:5000/sections/${sectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.$store.state.token}`
        },
        body: JSON.stringify(this.section)
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        // Redirect to section list page
        this.$router.push('/sections');
      })
      .catch(error => {
        console.error('Error updating section:', error);
        alert('An error occurred while updating the section');
      });
    }
  }
};
</script>

<style>
/* Add custom styles here */
</style>
