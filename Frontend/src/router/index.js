import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import store from '../store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {requiresAuth: true}
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/mybooks',
      name: 'mybooks',
      component: () => import('../views/MybooksView.vue')
    },
    {
      path: '/admin',
      name: 'admindashboard',
      component: () => import('../views/AdminView.vue')
    },
    {
      path: '/Testing',
      name: 'testing',
      component: () => import('../views/TestingView.vue')
    },
    {
      path: '/newbook',
      name: 'newbook',
      component: () => import('../views/NewBookView.vue')
    },
  ]
})

// Global navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const requiresAuth = to.meta.requiresAuth;

  if (requiresAuth && !isAuthenticated) {
    console.log('User not authenticated')
    alert('Login Required')
    // If route requires authentication and user is not authenticated, redirect to login
    next('/login');
  } else {
    // Otherwise, proceed to the route
    next();
  }
});

export default router
