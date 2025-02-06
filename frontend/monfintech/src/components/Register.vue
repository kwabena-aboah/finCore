<template>
  <main class="form-signin text-center">
    <form @submit.prevent="registerUser">
      <img src="@/assets/logo.jpeg" class="mb-4" alt="logo.jpeg" width="280" height="100">
      <div class="form-floating">
        <input v-model="form.username" type="text" class="form-control" id="username" placeholder="Username" required />
        <label for="username" class="form-label">Username</label>
      </div>
      <div class="form-floating">
        <input v-model="form.email" type="email" class="form-control" id="email" placeholder="Email" required />
        <label for="email" class="form-label">Email</label>
      </div>
      <div class="form-floating">
        <input v-model="form.password" type="password" class="form-control" id="password" placeholder="Password" required />
        <label for="password" class="form-label">Password</label>
      </div>
      <button type="submit" class="w-100 btn btn-lg btn-primary">Register</button>
    </form>
    <hr>
      <div class="checkbox mb-3">
        <p class="mt-5 mb-3 text-muted">Already have an account? Click on the "Sign In" button below.</p>
        <router-link to="/"  class="w-100 btn btn-lg btn-default shadow">Sign In</router-link>
      </div>
    <p class="mt-5 mb-3 text-muted">&copy; 2025–2026</p>
  </main>
</template>

<script>
import instance from '@/api/axios';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";


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
        toast.success("Registration successful!", response.data);
        // alert("Registration successful!");
        // console.log(response.data);
      } catch (error) {
        toast.success("Error during registration!", error.response.data);
        // console.error(error.response.data);
        // alert("Error during registration!");
      }
    },
  }
};
</script>
<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>