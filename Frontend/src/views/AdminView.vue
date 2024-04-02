<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">Book Requests</h1>
  
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>User</th>
            <th>Book</th>
            <th>Date Requested</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.user.username }}</td>
            <td>{{ request.book.name }}</td>
            <td>{{ formatDate(request.date_requested) }}</td>
            <td :class="getStatusClass(request.status)">{{ request.status }}</td>
            <td>
              <button
                v-if="request.status === 'Pending'"
                class="btn btn-success"
                @click="approveRequest(request.id)"
              >
                Approve
              </button>
              <button
                v-if="request.status === 'Pending'"
                class="btn btn-danger ml-2"
                @click="rejectRequest(request.id)"
              >
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        requests: [],
      };
    },
    mounted() {
      this.fetchRequests();
    },
    methods: {
      async fetchRequests() {
        try {
          const response = await fetch('http://localhost:5000/admin/requests'); // Update with your backend endpoint
          const data = await response.json();
          if (response.ok) {
            this.requests = data.requests;
          } else {
            throw new Error(data.message || 'Failed to fetch requests');
          }
        } catch (error) {
          console.error('Error fetching requests:', error);
        }
      },
      async approveRequest(requestId) {
        try {
          const response = await fetch(`/approve-request/${requestId}`, {
            method: 'PUT',
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            this.fetchRequests(); // Refresh the requests list
          } else {
            throw new Error(data.message || 'Failed to approve request');
          }
        } catch (error) {
          console.error('Error approving request:', error);
        }
      },
      async rejectRequest(requestId) {
        try {
          const response = await fetch(`/reject-request/${requestId}`, {
            method: 'PUT',
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            this.fetchRequests(); // Refresh the requests list
          } else {
            throw new Error(data.message || 'Failed to reject request');
          }
        } catch (error) {
          console.error('Error rejecting request:', error);
        }
      },
      formatDate(date) {
        return new Date(date).toLocaleDateString();
      },
      getStatusClass(status) {
        return {
          'text-success': status === 'Approved',
          'text-danger': status === 'Rejected',
          'text-warning': status === 'Pending',
        };
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add any custom styles here */
  </style>
  