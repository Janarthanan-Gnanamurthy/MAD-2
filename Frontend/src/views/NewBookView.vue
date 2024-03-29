<template>
    <div class="container mt-5">
      <h2>Add New Book</h2>
      <form @submit.prevent="addBook" class="mt-3">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input type="text" id="name" v-model="book.name" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Content:</label>
          <textarea id="content" v-model="book.content" class="form-control" required></textarea>
        </div>
        <div class="mb-3">
          <label for="author" class="form-label">Author:</label>
          <input type="text" id="author" v-model="book.author" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="date_issued" class="form-label">Date Issued:</label>
          <input type="date" id="date_issued" v-model="book.date_issued" class="form-control">
        </div>
        <div class="mb-3">
          <label for="return_date" class="form-label">Return Date:</label>
          <input type="date" id="return_date" v-model="book.return_date" class="form-control">
        </div>
        <div class="mb-3">
          <label for="section_id" class="form-label">Section ID:</label>
          <input type="number" id="section_id" v-model="book.section_id" class="form-control" required>
        </div>
        <div class="mb-3">
          <button type="submit" class="btn btn-primary">Add Book</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        book: {
          name: '',
          content: '',
          author: '',
          date_issued: '',
          return_date: '',
          section_id: ''
        },
        apiUrl: 'http://localhost:5000/books'  // Replace with your API URL
      };
    },
    methods: {
      async addBook() {
        try {
          const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.book)
          });
  
          const responseData = await response.json();
  
          if (response.ok) {
            alert('Book added successfully');  // Show success message
            this.book.name = '';  // Clear input fields
            this.book.content = '';
            this.book.author = '';
            this.book.date_issued = '';
            this.book.return_date = '';
            this.book.section_id = '';
          } else {
            alert(responseData.message || 'Failed to add book');  // Show error message
          }
        } catch (error) {
          console.error('Error adding book:', error);
          alert('An error occurred while adding the book');
        }
      }
    }
  };
</script>
  
  