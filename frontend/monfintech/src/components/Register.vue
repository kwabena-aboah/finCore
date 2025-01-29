<template>
  <div class="container mt-5">
    <h2>Register</h2>
    <form @submit.prevent="registerUser" class="form">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="form.username" type="text" class="form-control" id="username" required />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input v-model="form.email" type="email" class="form-control" id="email" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" id="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <br>
    <hr>
    <router-link to="/">Login</router-link>
  </div>
</template>

<script>
import instance from '@/api/axios';

export default {
  name: 'RegisterComponent',
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
      },
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await instance.post("auth/register/", this.form);
        alert("Registration successful!");
        console.log(response.data);
      } catch (error) {
        console.error(error.response.data);
        alert("Error during registration!");
      }
    },
  }
};
</script>