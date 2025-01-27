<template>
    <div>
        <Navbar />
        <div class="container mt-5">
            <h1>Welcome to MonFintech Dashboard</h1>
            <p>Manage your financial transactions, budget, and more!</p>
        </div>
    </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue"

export default {
    components: {
        Navbar,
    },
    name: 'DashboardPage',
}
</script>