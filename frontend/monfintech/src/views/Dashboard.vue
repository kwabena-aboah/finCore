<template>
    <div class="container mt-5">
        <h1>Welcome to Your Dashboard</h1>
        <p>You are successfully logged in.</p>
        <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
</template>

<script>
export default {
    name: 'DashboardPage',
    methods: {
        logout() {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            this.$router.push({ name: "LoginComponent" });
        }
    }
}
</script>