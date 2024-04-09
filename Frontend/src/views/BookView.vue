<template>
  <div>
    <iframe :src="pdfUrl" width="100%" height="800"></iframe>
  </div>
</template>

<script>
export default {
	props: {
		book_id: {
			type: Number,
      required: true				
		}
	},
  data() {
    return {
      pdfUrl: '', // Replace with logic to get your PDF URL
    }
  },
	async mounted(){
		await this.fetchBook()
	},
	methods: {
		async fetchBook(){
			try{
				let response = await fetch(`http://localhost:5000/get-book/${this.book_id}`, {
					method: 'GET',
					headers: {
						Authorization: `Bearer ${this.$store.state.token}`
					}
				})
				if (response.ok){
					let data = await response.json()
					console.log(data)
					this.pdfUrl = data.pdfurl
				}
				if (response.status == 404){
					console.log("Alert User doesn't Have access")
					alert("User doesn't have access")
					this.$router.push('/')
				}
			}catch (error) {
				console.log("error While book:", error)
			}
		}
	}
}
</script>
