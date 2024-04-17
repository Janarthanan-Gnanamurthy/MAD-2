<template>
  <div class="container">
    <h2 class="my-4">My Books</h2>

    <div class="card mb-4">
      <div class="card-header">
        <h3 class="mb-0">Currently Acquired</h3>
      </div>
      <ul class="list-group list-group-flush">
        <li v-for="book in acquiredBooks" :key="book.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ book.name }}
          <div>
            <button class="btn btn-primary mx-2" @click="$router.push(`/book/${book.id}`)" style="border-radius: 10px;">Read</button>
            <button class="btn btn-secondary mx-2" @click="openFeedbackModal(book.id)" style="border-radius: 10px;">Feedback</button>
            <button class="btn btn-success" @click="returnBook(book.id)" style="border-radius: 10px;">Return</button>
            <span class="mx-2">Return by {{ book.return_date }}</span>
          </div>
        </li>
        <li v-if="acquiredBooks.length === 0" class="list-group-item">You have no books currently acquired.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="mb-0">Completed Books</h3>
      </div>
      <ul class="list-group list-group-flush">
        <li v-for="book in returnedBooks" :key="book.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ book.name }}
          <span class="mx-2">Returned On {{ book.returned_on }}</span>
        </li>
        <li v-if="returnedBooks.length === 0" class="list-group-item">You have not returned any books yet.</li>
      </ul>
    </div>
    <div v-if="isFeedbackModalOpen" class="modal" tabindex="-1" role="dialog" style="display: block;">
      <div class="modal-dialog" role="document">
        <div class="modal-content"> 
          <div class="modal-header d-flex justify-content-between">
            <h5 class="modal-title">Feedback</h5>
            <button type="button" class="btn btn-danger close" @click="closeFeedbackModal">X</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="feedbackText">Feedback:</label>
              <textarea class="form-control" id="feedbackText" v-model="currentFeedback"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeFeedbackModal">Close</button>
            <button type="button" class="btn btn-primary" @click="feedBack">Save changes</button>
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
      acquiredBooks: [],
      returnedBooks: [],
      currentFeedback: '', // To store current feedback for modal
      selectedBookId: null,
      isFeedbackModalOpen: false
    };
  },
  mounted() {
    this.fetchUserBooks();
  },
  methods: {
    fetchUserBooks() {
      fetch('http://localhost:5000/user/books', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.acquiredBooks = data.acquired_books;
          this.returnedBooks = data.returned_books;
        })
        .catch(error => {
          console.error('Error fetching user books:', error);
        });
    },
    async returnBook(book_id){
      let response = await fetch(`http://localhost:5000/user/return/${book_id}`, {
        method: "PUT",
        headers:{
          'Authorization': `Bearer ${this.$store.state.token}`
        }
        
      })
      if (response.ok){
        data = await response.json()
        console.log(data.message)
        this.$router.go(0)
      }
    },
    openFeedbackModal(book_id) {
      this.selectedBookId = book_id;
      this.isFeedbackModalOpen = true; // Using jQuery to show Bootstrap modal
    },
    closeFeedbackModal() {
      this.isFeedbackModalOpen = false; // Hide the modal
    },
    async feedBack() {
      let response = await fetch(`http://localhost:5000/user/feedback/${this.selectedBookId}`, {
        method: "PUT",
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ feedback: this.currentFeedback })
      });

      if (response.ok) {
        let data = await response.json();
        console.log(data.message);
        this.isFeedbackModalOpen = false
      }
    },
  },
};
</script>

<style scoped>
.badge-danger {
  font-weight: bold;
}
</style>