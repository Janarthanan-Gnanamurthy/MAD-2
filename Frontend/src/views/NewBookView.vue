<template>
  <div class="container mt-5">
    <h2>Add New Book</h2>
    <form @submit.prevent="addBook" class="mt-3" enctype="multipart/form-data">
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
      <div class="form-group">
        <label for="section">Section: </label>
        <select class="form-control" id="section" v-model="book.section_id">
          <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="image" class="form-label">Image:</label>
        <input type="file" id="image" ref="image" class="form-control" accept="image/*">
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
      sections: [],
      book: {
        name: '',
        content: '',
        author: '',
        section_id: '',
        image: null  
      },
      apiUrl: 'http://localhost:5000/books'  
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async addBook() {
      try {
        const formData = new FormData();
        formData.append('name', this.book.name);
        formData.append('content', this.book.content);
        formData.append('author', this.book.author);
        formData.append('section_id', this.book.section_id);
        formData.append('file', this.$refs.image.files[0]);

        const response = await fetch(this.apiUrl, {
          method: 'POST',
          body: formData  
        });

        const responseData = await response.json();

        if (response.ok) {
          alert('Book added successfully');
          this.book.name = '';
          this.book.content = '';
          this.book.author = '';
          this.book.section_id = '';
          this.$refs.image.value = '';  
        } else {
          alert(responseData.message || 'Failed to add book');
        }
      } catch (error) {
        console.error('Error adding book:', error);
        alert('An error occurred while adding the book');
      }
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
  }
};
</script>
