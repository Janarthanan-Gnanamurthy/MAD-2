<template>
  <div class="container">
		<div class="row justify-content-center p-5">
			<div class="col-md-6 bgc-2 p-4 rounded border-0 rounded-lg shadow">
				<h2 class="text-center mb-3">Create Account</h2>
				<div class="my-3">
					<input
						type="text"
						class="form-control"
						v-model="name"
						placeholder="Name"
						required
					/>
				</div>

				<div class="mb-3">
					<input
						type="number"
						class="form-control"
						v-model="number"
						placeholder="Number"
						minlength="10"
						maxlength="10"
						required
					/>
				</div>

				<div class="mb-3">
					<input
						type="email"
						class="form-control"
						v-model="email"
						placeholder="Email"
						required
					/>
				</div>

				<div class="mb-5">
					<input
						type="password"
						class="form-control"
						v-model="password"
						placeholder="Password"
						minlength="8"
						maxlength="16"
						required
					/>
				</div>

				<button type="submit" class="btn btn-primary align-self-center">
					Register
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data(){
		return {
			name: '',
			email: '',
			number: '',
			passworda: ''
		}
	},
	methods: {
		createUser(){
			return -1
		}
	}
}
</script>