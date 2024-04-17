<template>
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h1 class="my-4">Dashboard</h1>
        </div>
      </div>
      <div class="row" >
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">Total Users</div>
            <div class="card-body">
              <div class="d-flex justify-content-center">
                <div class="chart-container">
                  <canvas ref="totalUsersChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">User Activity by Month</div>
            <div class="card-body">
              <div class="d-flex justify-content-center">
                <div class="chart-container">
                  <canvas ref="userActivityChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">Books by Section</div>
            <div class="card-body">
              <div class="d-flex justify-content-center">
                <div class="chart-container">
                  <canvas ref="booksBySectionChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header">Top 10 Books</div>
            <div class="card-body">
              <ol>
                <li v-for="book in topBooks" :key="book.id">{{ book.title }}</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'AdminStats',
    data() {
      return {
				totalUsersData: [
					{ "date": "2022-01-01", "count": 100 },
					{ "date": "2022-02-01", "count": 120 },
					{ "date": "2022-03-01", "count": 150 },
					{ "date": "2022-04-01", "count": 180 },
					{ "date": "2022-05-01", "count": 200 },
					{ "date": "2022-06-01", "count": 220 }
				],
				userActivityData: [
					{ "month": "January", "count": 500 },
					{ "month": "February", "count": 600 },
					{ "month": "March", "count": 700 },
					{ "month": "April", "count": 800 },
					{ "month": "May", "count": 900 },
					{ "month": "June", "count": 1000 }
				],
				booksBySectionData: [
					{ "section": "Fiction", "count": 200 },
					{ "section": "Non-Fiction", "count": 150 },
					{ "section": "Biography", "count": 100 },
					{ "section": "Science", "count": 80 },
					{ "section": "Technology", "count": 120 },
					{ "section": "History", "count": 90 }
				],
				topBooks: [
					{ "id": 1, "title": "The Great Gatsby" },
					{ "id": 2, "title": "To Kill a Mockingbird" },
					{ "id": 3, "title": "1984" },
					{ "id": 4, "title": "Pride and Prejudice" },
					{ "id": 5, "title": "The Catcher in the Rye" },
					{ "id": 6, "title": "The Hobbit" },
					{ "id": 7, "title": "The Lord of the Rings" },
					{ "id": 8, "title": "Harry Potter and the Sorcerer's Stone" },
					{ "id": 9, "title": "The Chronicles of Narnia" },
					{ "id": 10, "title": "The Alchemist" }
				]
      };
    },
    mounted() {
      this.fetchAdminStats();
			// this.renderCharts()
    },
    methods: {
      async fetchAdminStats() {
        try {
          const response = await fetch('http://localhost:5000/adminstats', {
            headers: {
              Authorization: `Bearer ${this.jwtToken}`,
            },
          });
          const adminData = await response.json();
          console.log(adminData)
          // this.totalUsersData = adminData.totalUsers;
          this.userActivityData = adminData.userActivity;
          this.booksBySectionData = adminData.booksBySection;
          this.topBooks = adminData.topBooks;
          this.renderCharts();
        } catch (error) {
          console.error('Error fetching admin stats:', error);
        }
      },
      renderCharts() {
        // const totalUsersCtx = this.$refs.totalUsersChart.getContext('2d');
        // const totalUsersChart = new Chart(totalUsersCtx, {
        //   type: 'line',
        //   data: {
        //     labels: this.totalUsersData.map(item => item.date),
        //     datasets: [
        //       {
        //         label: 'Total Users',
        //         data: this.totalUsersData.map(item => item.count),
        //         backgroundColor: 'rgba(54, 162, 235, 0.5)',
        //         borderColor: 'rgba(54, 162, 235, 1)',
        //         borderWidth: 1,
        //       },
        //     ],
        //   },
        // });
  
        const userActivityCtx = this.$refs.userActivityChart.getContext('2d');
        const userActivityChart = new Chart(userActivityCtx, {
          type: 'doughnut',
          data: {
            labels: this.userActivityData.map(item => item.month),
            datasets: [
              {
                data: this.userActivityData.map(item => item.count),
                backgroundColor: [
                  '#FF6384',
                  '#36A2EB',
                  '#FFCE56',
                  '#5cb85c',
                  '#d9534f',
                  '#f0ad4e',
                ],
              },
            ],
          },
        });
  
        const booksBySectionCtx = this.$refs.booksBySectionChart.getContext('2d');
        const booksBySectionChart = new Chart(booksBySectionCtx, {
          type: 'pie',
          data: {
            labels: this.booksBySectionData.map(item => item.section),
            datasets: [
              {
                data: this.booksBySectionData.map(item => item.count),
                backgroundColor: [
                  '#FF6384',
                  '#36A2EB',
                  '#FFCE56',
                  '#5cb85c',
                  '#d9534f',
                  '#f0ad4e',
                ],
              },
            ],
          },
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .chart-container {
    max-width: 500px;
    max-height: 400px;
  }
  </style>