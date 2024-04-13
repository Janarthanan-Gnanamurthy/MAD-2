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
				const response = await fetch('http://localhost:5000/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(FormData),
        });

				if (response.status === 401 ){
					alert('No Admin Previledges')
				}
				else if (!response.ok) {
          alert('Login Failed')
          throw new Error('Login failed');
        }

        const data = await response.json();
        const token = data.access_token;
        sessionStorage.setItem('jwt_token', token);
        this.$store.commit('AUTH_SUCCESS', token);

				this.$router.push('/admin');
			} catch (error) {
				console.error('Login Error:', error.message);
			}
		}
	}
}
</script>