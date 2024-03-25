<template>
	<main class="d-flex justify-content-center align-items-center p-5">
		<div class="card border-0 rounded-lg bgc-2 shadow p-4" style="width: 450px">
			<h1 class="text-center mt-1 t4 mb-4">User Login</h1>
			<div class="form-group mb-3">
				<h5 for="number" class="from-label text-white t4">Username:</h5>
				<input
					type="text"
					class="nm form-control rounded w-100"
					placeholder="Enter Username"
					v-model="name"
					required
				/>
			</div>
			<div class="form-group mb-3">
				<h5 for="password" class="form-label text-white t4">Password:</h5>
				<input
					type="password"
					class="nm form-control rounded w-100"
					placeholder="Enter password"
					v-model="password"
					required
				/>
			</div>
			<button @click="login" class="btn btn-primary rounded w-100 mt-3">
				Sign In
			</button>
			<p class="mt-3 text-center">
				New to ECHO?
				<a href="/Register">Sign up</a>
			</p>

		</div>
	</main>
</template>

<script>
export default {
	data(){
		return {
			name: '',
			email: '',
			number: '',
			password: ''
		}
	},
	methods: {
		async login(){
			const FormData = {username: this.name, password: this.password}
			try {
				const response = await fetch(`http://localhost:5000/login`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(FormData)
				});

				if (!response.ok) {
						throw new Error(`HTTP error! Status: ${response.status}`);
				}

				const data = await response.json();
				this.$store.commit('updateUser', data)
				console.log('success', data);
			} catch (error) {
				console.error('Error fetching User:', error);
				alert('Error fetching User. Please try again.');
			}
		}
	}
}
</script>