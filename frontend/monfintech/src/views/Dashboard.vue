<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Welcome to MonFintech Dashboard</h1>
            <p>Manage your financial transactions, budget, and more!</p>
        </main>
    </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue"
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: 'DashboardPage',
    created() {
        toast.success("Login successful!", {
          autoClose: 8000,
        });
    },
}
</script>