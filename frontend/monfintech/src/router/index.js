import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/Login.vue";
import RegisterComponent from "@/components/Register.vue";
import store from "@/store";

const routes = [
    {
        path: "/",
        name: "LoginComponent",
        component: LoginComponent
    },
    {
        path: "/register",
        name: "RegisterComponent",
        component: RegisterComponent
    },
    {
        path: '/dashboard',
        name: 'DashboardPage',
        component: () => import('../views/Dashboard.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/profile',
        name: 'ProfilePage',
        component: () => import('../views/Profile.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/transactions',
        name: 'TransactionsPage',
        component: () => import('../views/Transactions.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/budgets',
        name: 'BudgetPage',
        component: () => import('../views/Budget.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/assets',
        name: 'PortfolioPage',
        component: () => import('../views/Portfolio.vue'),
        meta: { requiresAuth: true },
    },
];

const router  = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated;
    if (to.meta.requiresAuth && !isAuthenticated) {
        next({ name: "LoginComponent" });
    } else {
        next();
    }
});

export default router;