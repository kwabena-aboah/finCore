import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/Login.vue";
import RegisterComponent from "@/components/Register.vue";

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
];

const router  = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem("access_token") !== null;
    if (to.meta.requiresAuth && !isAuthenticated) {
        next({ name: "LoginComponent" });
    } else {
        next();
    }
});

export default router;