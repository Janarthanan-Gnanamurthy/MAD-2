<template>
  <div class="container my-5">
    <div class="row">
      <!-- Section List -->
      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-header">
            <h3 class="mb-0">Sections</h3>
          </div>
          <div class="list-group list-group-flush">
            <a
              v-for="section in sections"
              :key="section.id"
              href="#"
              class="list-group-item list-group-item-action"
              :class="{ 'active': section.isActive }"
              @click.prevent="toggleSection(section)"
            >
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">{{ section.name }}</h5>
                <span class="badge badge-primary badge-pill">{{ section.books.length }}</span>
              </div>
            </a>
          </div>
        </div>
      </div>
      <!-- Book List -->
      <div class="col-md-9">
        <div class="row">
          <div
            v-for="section in sections"
            :key="section.id"
            class="col-md-12 mb-4"
            v-show="section.isActive"
          >
            <h4 class="mb-3">{{ section.name }}</h4>
            <p>{{ section.description }}</p>
            <div class="row">
              <div
                v-for="book in section.books"
                :key="book.id"
                class="col-md-4 mb-4"
              >
                <div class="card h-100">
                  <img
                    :src="'http://localhost:5000/uploads/books/' + book.image_filename"
                    class="card-img-top"
                    alt="Book Cover"
                  />
                  <div class="card-body">
                    <h5 class="card-title">{{ book.name }}</h5>
                    <div class="btn-group">
                      <button
                        v-if="!isBookBorrowed(book.id)"
                        class="btn btn-primary"
                        @click="borrowBook(book.id)"
                      >
                        Borrow
                      </button>
                      <button
                        v-else
                        class="btn btn-success"
                        @click="$router.push(`/book/${book.id}`)"
                      >
                        Read
                      </button>
                      <button
                        v-if="isBookBorrowed(book.id)"
                        class="btn btn-warning"
                        @click="returnBook(book.id)"
                      >
                        Return
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
 </template>
 
 <script>
 export default {
  data() {
    return {
      sections: [],
      borrowedBooks: []
    };
  },
  async mounted() {
    try {
      let response = await fetch("http://localhost:5000/sections", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      });
      if (response.ok) {
        let data = await response.json();
        console.log(data);
        this.sections = data.sections.map(section => ({
          ...section,
          isActive: false
        }));
        this.sections[0].isActive = true; // Show the first section by default
        this.borrowedBooks = data.userBooks;
      } else {
        // Check if the error is "unauthorized"
        if (response.status === 401) {
          this.$store.dispatch('logout');
          alert("Login required");
          this.$router.push({ name: 'login' });
        }
      }
    } catch (error) {
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
    async returnBook(book_id) {
      let response = await fetch(`http://localhost:5000/user/return/${book_id}`, {
        method: "PUT",
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      });
      if (response.ok) {
        alert("Book returned Successfully");
        data = await response.json();
        console.log(data.message);
        this.$router.go(0);
      }
    },
    toggleSection(section) {
      this.sections.forEach(s => (s.isActive = false));
      section.isActive = true;
    }
  }
 };
 </script>
 
 <style>
 .card {
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
 }
 
 .card-header {
  background-color: #f8f9fa;
 }
 
 .list-group-item-action {
  cursor: pointer;
 }
 
 .list-group-item-action.active {
  background-color: #007bff;
  color: #fff;
 }
 
 .card-img-top {
  height: 200px;
  object-fit: cover;
 }
 
 .btn-group > .btn {
  margin-right: 0.5rem;
 }
 </style>