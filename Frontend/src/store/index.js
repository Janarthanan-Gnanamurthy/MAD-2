import { createStore } from 'vuex';

export default createStore({
  state: {
    token: sessionStorage.getItem('jwt_token') || '',
    status: '',
  },
  mutations: {
    AUTH_SUCCESS(state, token) {
      state.token = token;
      state.status = 'success';
    },
    AUTH_ERROR(state) {
      state.token = '';
      state.status = 'error';
    },
    LOGOUT(state) {
      state.token = '';
      state.status = '';
    },
  },
  actions: {
    async login({ commit }, user) {
      try {
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(user),
        });

        if (!response.ok) {
          alert('Login Failed')
          throw new Error('Login failed');
        }

        const data = await response.json();
        const token = data.access_token;
        sessionStorage.setItem('jwt_token', token);
        commit('AUTH_SUCCESS', token);
      } catch (error) {
        sessionStorage.removeItem('jwt_token');
        commit('AUTH_ERROR');
        throw error;
      }
    },
    logout({ commit }) {
      sessionStorage.removeItem('jwt_token');
      commit('LOGOUT');
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    authStatus: (state) => state.status,
  },
});
