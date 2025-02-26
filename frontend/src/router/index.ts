import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import BashoView from '../views/BashoView.vue';
import YearView from '../views/YearView.vue'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { breadcrumb: [{ name: 'Home', path: '/' }] },
    },
    {
      path: '/basho',
      name: 'basho',
      component: BashoView,
      meta: { breadcrumb: [{ name: 'Home', path: '/' }, { name: 'Basho', path: '/basho' }] },
    },
    {
      path: '/basho/year',  // This is a sibling route to `/basho`, accessible from `/basho/year`
      name: 'year',
      component: YearView,
      meta: { breadcrumb: [{ name: 'Home', path: '/' }, { name: 'Basho', path: '/basho' }, { name: 'Year', path: '' }] },
    },
  ],
});

export default router;
