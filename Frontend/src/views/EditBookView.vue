<template>
  <div class="container mt-5">
    <h2>Edit Book</h2>
    
    <form @submit.prevent="updateBook" class="mt-4">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" class="form-control" id="name" v-model="book.name">
      </div>
      
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea class="form-control" id="content" rows="5" v-model="book.content"></textarea>
      </div>
      
      <div class="form-group">
        <label for="author">Author:</label>
        <input type="text" class="form-control" id="author" v-model="book.author">
      </div>
      
      <div class="form-group">
        <label for="section">Section: </label>
        <select class="form-control" id="section" v-model="book.section_id">
          <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
        </select>
      </div>
      
      <button type="submit" class="btn btn-primary my-2">Update</button>
    </form>
    
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      book: {
        id: null,
        name: '',
        content: '',
        author: '',
        section_id: null
      },
      sections: [],
      errorMessage: ''
    };
  },
  created() {
    const bookId = this.$route.params.id;
    this.fetchBook(bookId);
    this.fetchSections();
  },
  methods: {
    fetchBook(bookId) {
      fetch(`http://localhost:5000/books/${bookId}`, {
				headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        },
			})
        .then(response => {
          if (!response.ok) {
            throw new Error('Book not found');
          }
          return response.json();
        })
        .then(data => {
          this.book = data;
        })
        .catch(error => {
          console.error('Error fetching book:', error);
        });
    },
    fetchSections() {
      fetch('http://localhost:5000/sections', {
				headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        },
			})
        .then(response => {
          if (!response.ok) {
            throw new Error('Sections not found');
          }
          return response.json();
        })
        .then(data => {
          this.sections = data.sections;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    updateBook() {
      fetch(`http://localhost:5000/books/${this.book.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
					'Authorization': `Bearer ${this.$store.state.token}`
        },
        body: JSON.stringify(this.book)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error updating book');
          }
          return response.json();
        })
        .then(data => {
          console.log('Book updated successfully:', data);
          // Redirect or show a success message
          this.$router.push('/');  // Assuming you have a route named 'BookList' for listing books
        })
        .catch(error => {
          this.errorMessage = 'Error updating book: ' + error.message;
          console.error('Error updating book:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
