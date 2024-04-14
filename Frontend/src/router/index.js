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
      path: '/search',
      name: 'searchresults',
      component: () => import('../views/SearchResultsView.vue')
    },
    {
      path: '/mybooks',
      name: 'mybooks',
      component: () => import('../views/MybooksView.vue')
    },
    {
      path: '/book/:book_id',
      name: 'book',
      component: () => import('../views/BookView.vue'),
      props:true
    },
    {
      path: '/admin',
      name: 'admindashboard',
      component: () => import('../views/AdminView.vue')
    },
    {
      path: '/admin/login',
      name: 'adminlogin',
      component: () => import('../views/AdminLoginView.vue')
    },
    {
      path: '/admin/section/edit/:id',
      name: 'sectionedit',
      component: () => import('../views/EditSectionView.vue')
    },
    {
      path: '/admin/book/edit/:id',
      name: 'bookedit',
      component: () => import('../views/EditBookView.vue')
    },
    {
      path: '/admin/stats',
      name: 'adminstats',
      component: () => import('../views/AdminStatsView.vue')
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
