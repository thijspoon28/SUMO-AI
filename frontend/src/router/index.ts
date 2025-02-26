import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BashosView from '../views/BashosView.vue';
import YearView from '../views/YearView.vue'; 
import BashoView from '@/views/BashoView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { breadcrumb: [
        { name: 'Home', path: '/' }
      ] },
    },
    {
      path: '/bashos',
      name: 'bashos',
      component: BashosView,
      meta: { breadcrumb: [
        { name: 'Home', path: '/' }, 
        { name: 'Bashos', path: '/bashos' }
      ] },
    },
    {
      path: '/bashos/:year',  
      name: 'year',
      component: YearView,
      meta: { breadcrumb: [
        { name: 'Home', path: '/' }, 
        { name: 'Bashos', path: '/bashos' }, 
        { name: 'Year', path: '' }
      ] },
      props: true,
    },
    {
      path: '/bashos/:year/:basho',  
      name: 'basho',
      component: BashoView,
      meta: { breadcrumb: [
        { name: 'Home', path: '/' }, 
        { name: 'Bashos', path: '/bashos' }, 
        { name: 'Year', path: '/bashos/:year' },
        { name: 'basho', path: ''}
      ] },
      props: true,
    },
  ],
});

export default router;
