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
            <button class="btn btn-primary mx-2" @click="$router.push(`/book/${book.id}`)" >Read</button>
            <button class="btn btn-success" @click="returnBook(book.id)" >Return</button>
            <span class="mx-2">Return by {{ book.return_date }}</span>
            <span v-if="isOverdue(book.return_date)" class="badge badge-danger">Overdue</span>
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
        <li v-for="book in returnedBooks" :key="book.id" class="list-group-item">{{ book.name }}</li>
        <li v-if="returnedBooks.length === 0" class="list-group-item">You have not returned any books yet.</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      acquiredBooks: [],
      returnedBooks: [],
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
      }
    },
    isOverdue(returnDate) {
      const today = new Date();
      const dueDate = new Date(returnDate);
      dueDate.setDate(dueDate.getDate() + 7);
      return today > dueDate;
    },
  },
};
</script>

<style scoped>
.badge-danger {
  font-weight: bold;
}
</style>