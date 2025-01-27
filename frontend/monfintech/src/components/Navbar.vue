<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">MonFintech</router-link>
            <button 
                type="button"
                class="navbar-toggler"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link to="/dashboard" class="nav-link">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/profile" class="nav-link">Profile</router-link>
                    </li>
                </ul>
                <button class="btn btn-danger" @click="logout">Logout</button>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: "NavbarComponent",
    methods: {
        logout() {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            this.$router.push({ name: "LoginComponent" });
        }
    }
};
</script>

<style>
.navbar {
    margin-bottom: 20px;
}
</style>