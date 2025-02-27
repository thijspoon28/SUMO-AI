import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BashosView from '../views/BashosView.vue';
import YearView from '../views/YearView.vue';
import BashoView from '@/views/BashoView.vue';
import LoginView from '@/views/LoginView.vue';
import AdminView from '@/views/AdminView.vue';
import { useAuthStore } from '@/stores/auth';
import AccountView from '@/views/AccountView.vue';
import NotFoundView from '@/views/NotFoundView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' }
        ]
      },
    },
    {
      path: '/404',
      name: 'not-found',
      component: NotFoundView,
      meta: {},
    },
    {
      path: '/bashos',
      name: 'bashos',
      component: BashosView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Bashos', path: '/bashos' }
        ]
      },
    },
    {
      path: '/bashos/:year',
      name: 'year',
      component: YearView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Bashos', path: '/bashos' },
          { name: 'Year', path: '' }
        ]
      },
      props: true,
    },
    {
      path: '/bashos/:year/:basho',
      name: 'basho',
      component: BashoView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Bashos', path: '/bashos' },
          { name: 'Year', path: '/bashos/:year' },
          { name: 'basho', path: '' }
        ]
      },
      props: true,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Login', path: '/login' }
        ]
      },
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Account', path: '/account' }
        ],
        requiresAuth: true,
      },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: {
        breadcrumb: [
          { name: 'Home', path: '/' },
          { name: 'Admin', path: '/admin' }
        ],
        // requiresAuth: true,
        requiresAdmin: true,
      },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
  }
  
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!authStore.isAdmin()) {
      next({ path: '/404' })
      return
    }
  }
  
  next()
})

export default router;
