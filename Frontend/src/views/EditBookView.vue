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
				<label for="section_id">Section ID:</label>
				<input type="number" class="form-control" id="section_id" v-model.number="book.section_id">
			</div>
			
			<button type="submit" class="btn btn-primary">Update</button>
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
			errorMessage: ''
		};
	},
	created() {
		const bookId = this.$route.params.id;
		this.fetchBook(bookId);
	},
	methods: {
		fetchBook(bookId) {
			fetch(`http://localhost:5000/books/${bookId}`, {
				headers: {
					'Authorization': `Bearer ${this.$store.state.token}`
				}
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
					this.$router.push('/'); 
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
