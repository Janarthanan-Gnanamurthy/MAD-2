<template>
	<main class="d-flex justify-content-center align-items-center p-5">
		<div class="card border-0 rounded-lg bgc-2 shadow p-4" style="width: 450px">
			<h1 class="text-center mt-1 t4 mb-4">Admin Login</h1>
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
					@keyup.enter="login"
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
				await this.$store.dispatch('login', FormData);
				this.$router.push('/');
			} catch (error) {
				console.error('Login Error:', error.message);
			}
		}
	}
}
</script>