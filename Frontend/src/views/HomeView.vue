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
            <span class="badge badge-primary badge-pill">{{ section.books.length }}</span>
          </li>
        </ul>
      </div>
      <!-- Book List -->
      <div class="col-md-8">
        <h3 v-if="selectedSection">Books in {{ selectedSection.name }}</h3>
        
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
            <span v-if="!isBookBorrowed(book.id)" class="btn btn-primary " @click="borrowBook(book.id)">Borrow</span>
            <span v-else class="badge badge-danger badge-pill text-black" @click="returnBook(book)">Return</span>
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
      borrowedBooks: []  // List of borrowed book ids
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
        this.sections = data;
        this.selectedSection = this.sections[0];
      } else {
        // Check if the error is "unauthorized"
        if (response.status === 401) {
          alert("Login required")
          this.$router.push({ name: 'login' });
        }
      }
    }catch (error) {
      console.error("Error Fetching:", error);
    }
  },
  methods: {
    isBookBorrowed(bookId) {
      return this.borrowedBooks.includes(bookId);
    },
    async borrowBook(bookId) {
      const data = {
            book_id: bookId
        };
        try {
          const response = await fetch('http://localhost:5000/request-book', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.$store.state.token}`
            },
            body: JSON.stringify(data),
          });

          const responseData = await response.json();

          if (response.ok) {
            alert(responseData.message);
          } else {
            throw new Error(responseData.message || 'Failed to request book');
          }
        } catch (error) {
          console.error("Error requesting book:", error);
        }
    },
    returnBook(book) {
      // Simulate returning a book (you can replace this with an actual API call)
      const index = this.borrowedBooks.indexOf(book.id);
      if (index > -1) {
        this.borrowedBooks.splice(index, 1);
      }
      alert(`You have returned the book: ${book.name}`);
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
