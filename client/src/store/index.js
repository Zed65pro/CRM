import { createStore } from "vuex";
export default createStore({
  state: {
    isLoading: false,
    isAuthenticated: false,
    token: "",
    user: {
      username: "",
      email: "",
      id: 0,
      is_staff: false,
    },
  },
  getters: {},
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("token")) {
        if (localStorage.getItem("user")) {
          state.user = JSON.parse(localStorage.getItem("user"));
        }
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;
      } else {
        state.token = "";
        state.isAuthenticated = false;
      }
    },
    setIsLoading(state, status) {
      state.isLoading = status;
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = "";
      state.isAuthenticated = false;
    },
    setUser(state, user) {
      state.user = user;
    },
    removeUser(state) {
      state.user = {
        username: "",
        email: "",
        id: 0,
        is_staff: false,
      };
    },
  },
  actions: {},
  modules: {},
});
