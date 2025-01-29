<template>
    <div class="container mt-5">
        <h2>Login</h2>
        <form @submit.prevent="loginUser" class="form">
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input v-model="form.username" type="text" class="form-control" id="username" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="form.password" type="password" class="form-control" id="password" required />
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <br>
        <hr>
        <router-link to="/register">Register</router-link>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { mapActions } from 'vuex';

export default {
    name: 'LoginComponent',
    data() {
        return {
            form: {
                username: "",
                password: "",
            },
        };
    },
    methods: {
        ...mapActions(["saveTokens"]),
        async loginUser() {
            try {
                const response = await instance.post("auth/token/", this.form);
                const { access, refresh } = response.data;
                
                // save token in vuex store
                this.saveTokens({ accessToken: access, refreshToken: refresh });
                
                alert("Login successful!");
                this.$router.push({ name: "DashboardPage" });
            } catch (error) {
                console.error(error.response.data);
                alert("Invalid credentials")
            }
        },
    },
};
</script>