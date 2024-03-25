import { createStore } from 'vuex';

export default createStore({
  state: {
    user: {'jana': 'AI-DS'},
  },
  mutations: {
    updateUser(state, user){
        state.user = user
    }
  },
  actions: {

  }
});
