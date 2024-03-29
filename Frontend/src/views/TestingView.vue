<template>
    <div class="container mt-5">
      <h2>Add New Section</h2>
      <form @submit.prevent="addSection" class="mt-3">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input type="text" id="name" v-model="section.name" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description:</label>
          <textarea id="description" v-model="section.description" class="form-control" required></textarea>
        </div>
        <div class="mb-3">
          <button type="submit" class="btn btn-primary">Add Section</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        section: {
          name: '',
          description: ''
        },
        apiUrl: 'http://localhost:5000/sections'  
      };
    },
    methods: {
      async addSection() {
        try {
          const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.section)
          });
  
          const responseData = await response.json();
  
          if (response.ok) {
            alert(responseData.message);  // Show success message
            this.section.name = '';  // Clear input fields
            this.section.description = '';
          } else {
            alert(responseData.message || 'Failed to add section');  // Show error message
          }
        } catch (error) {
          console.error('Error adding section:', error);
          alert('An error occurred while adding the section');
        }
      }
    }
  };
</script>
  
  