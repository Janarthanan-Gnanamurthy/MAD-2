<template>
  <div class="container mt-5">
    
    <div class="row">
      <!-- Section List -->
      <div class="col-md-4">
        <h3>Sections</h3>
        <ul class="list-group">
          <li 
            v-for="section in sections" 
            :key="section.id" 
            class="list-group-item d-flex justify-content-between align-items-center"
            @click="selectedSection = section"
            :class="{ 'active': selectedSection && selectedSection.id === section.id }"
          >
            {{ section.name }}
            <div>
              
              <button class="btn btn-warning mx-2" @click='$router.push(`admin/section/edit/${section.id}`)' style="border-radius: 10px;">Edit</button>
              <button v-if="!section.books.length" class="btn btn-danger mx-2" @click="deleteBook(book.id)" style="border-radius: 10px;">Delete</button>
              <span class="badge bg-secondary badge-pill " style="border-radius: 10px;">{{ section.books.length }}</span>
            </div>
          </li>
        </ul>
      </div>
      <!-- Book List -->
      <div class="col-md-8">
        <h3 v-if="selectedSection">{{ selectedSection.name }}</h3>
        <h5 v-if="selectedSection" class="mb-4">{{ selectedSection.description }}</h5>
        
        <ul v-if="selectedSection" class="list-group">
          <li 
            v-for="book in selectedSection.books" 
            :key="book.id" 
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div class="d-flex align-items-center">
              <img 
                :src="'http://localhost:5000/uploads/books/' + book.image_filename" 
                alt="Book Cover" 
                style="height: 50px; margin-right: 10px;"
              >
              {{ book.name }}
            </div>
            <div>
              <!-- <button class="btn btn-success mx-2" @click='$router.push(`/book/${book.id}`)'>Read</button> -->
              <button class="btn btn-warning mx-2" @click='$router.push(`admin/book/edit/${book.id}`)'>Edit</button>
              <button class="btn btn-danger mx-2" @click="deleteBook(book.id)">Delete</button>
            </div>
          </li>
        </ul> 
      </div>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sections: [],
      selectedSection: null,
      borrowedBooks: [] 
    };
  },
  async mounted() {
    try{
      let response = await fetch("http://localhost:5000/sections",  {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.$store.state.token}`
            }})
      if (response.ok) {
        let data = await response.json();
        console.log(data)
        this.sections = data.sections;
        this.selectedSection = this.sections[0];
        this.borrowedBooks = data.userBooks;
      } else {
        // Check if the error is "unauthorized"
        if (response.status === 401) {
          this.$store.dispatch('logout')
          alert("Login required")
          this.$router.push({ name: 'login' });
        }
      }
    }catch (error) {
      console.error("Error Fetching:", error);
    }
  },
  methods: {
    async deleteBook(bookId) {
      const url = `http://localhost:5000/books/${bookId}`;  // Replace with your actual API endpoint
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,  // Adjust based on authentication method
        },
      });

      if (!response.ok) {
        throw new Error(`Error deleting book: ${await response.text()}`);
      }

      const data = await response.json();
      console.log('Book deleted:', data);

      // Handle success or error in your component
      // For example:
      if (data.message === "Book deleted successfully") {
        alert("Book successfully deleted")
        this.$router.push.get(0)
      } else {
        // Show error message
      }
    }
  }
};
</script>

<style>
/* Add custom styles here */
.active {
  background-color: #007bff;
  color: white;
}
</style>
