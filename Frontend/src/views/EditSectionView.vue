<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Edit Section</h1>
    
    <form @submit.prevent="updateSection" class="col-md-8 offset-md-2">
      <div class="form-group">
        <label for="name">Section Name:</label>
        <input type="text" class="form-control" id="name" v-model="section.name" required>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea class="form-control" id="description" v-model="section.description" rows="3"></textarea>
      </div>
      <div class="form-group">
        <label for="books">Books:</label>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Select</th>
              <th>Name</th>
              <th>Author</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in allBooks" :key="book.id">
              <td>
                <input type="checkbox" :value="book.id" v-model="selectedBooks">
              </td>
              <td>{{ book.name }}</td>
              <td>{{ book.author }}</td>
            </tr>
          </tbody>
        </table>
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
      },
      allBooks: [],
      selectedBooks: []
    };
  },
  mounted() {
    // Fetch section data by ID from the backend
    const sectionId = this.$route.params.id;
    fetch(`http://localhost:5000/sections/${sectionId}`, {
      headers: {
        'Authorization': `Bearer ${this.$store.state.token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      this.section = data;
      this.selectedBooks = this.section.books.map(book => book.id);
    });

    // Fetch all books from the backend
    fetch('http://localhost:5000/books', {
      headers: {
        'Authorization': `Bearer ${this.$store.state.token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      this.allBooks = data;
    });
  },
  methods: {
    updateSection() {
      const sectionId = this.$route.params.id;
      
      fetch(`http://localhost:5000/sections/${sectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.$store.state.token}`
        },
        body: JSON.stringify({
          name: this.section.name,
          description: this.section.description,
          book_ids: this.selectedBooks
        })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        // Redirect to section list page
        this.$router.push('/');
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
