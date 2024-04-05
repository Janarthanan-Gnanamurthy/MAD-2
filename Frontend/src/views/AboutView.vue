<template>
  <div class="container">
    <h1 class="my-4">User Stats</h1>
    <div class="row">
      <div class="col-md-6">
        <div class="card mb-4">
          <div class="card-header">Books Read</div>
          <div class="card-body">
            <div class="d-flex justify-content-center">
              <div class="chart-container">
                <canvas ref="booksReadChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card mb-4">
          <div class="card-header">Section Distribution</div>
          <div class="card-body">
            <div class="d-flex justify-content-center">
              <div class="chart-container">
                <canvas ref="sectionDistributionChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'UserStats',
  data() {
    return {
      booksReadData: [
        { section: 'Fiction', count: 5 },
        { section: 'Science', count: 2 },
        { section: 'History', count: 3 },
      ],
      sectionDistributionData: [
        { section: 'Completed', count: 7 },
        { section: 'In Progress', count: 2 },
        { section: 'To Read', count: 1 },
      ],
    };
  },
  mounted() {
    this.renderCharts();
  },
  methods: {
    renderCharts() {
      const booksReadCtx = this.$refs.booksReadChart.getContext('2d');
      const booksReadChart = new Chart(booksReadCtx, {
        type: 'bar',
        data: {
          labels: this.booksReadData.map(item => item.section),
          datasets: [
            {
              label: 'Books Read',
              data: this.booksReadData.map(item => item.count),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
            },
          ],
        },
      });

      const sectionDistributionCtx = this.$refs.sectionDistributionChart.getContext('2d');
      const sectionDistributionChart = new Chart(sectionDistributionCtx, {
        type: 'doughnut',
        data: {
          labels: this.sectionDistributionData.map(item => item.section),
          datasets: [
            {
              data: this.sectionDistributionData.map(item => item.count),
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
