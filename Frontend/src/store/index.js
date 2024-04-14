import { createStore } from 'vuex';

export default createStore({
  state: {
    user: JSON.parse(sessionStorage.getItem('userData')) || null,
    token: sessionStorage.getItem('jwt_token') || '',
    status: '',
  },
  mutations: {
    USER_UPDATE(state, user) {
      state.user = user;
      sessionStorage.setItem('userData', JSON.stringify(user));
    },
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
        console.log(data)
        const token = data.access_token;
        sessionStorage.setItem('jwt_token', token);
        commit('USER_UPDATE', data.userData);
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
