<template>
    <div>
        <Navbar />
        <div class="container" mt-5>
            <h2>Your Profile</h2>
            <p>Username: {{ user.username }}</p>
            <p>Email: {{ user.email }}</p>
        </div>
    </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
    name: "ProfilePage",
    components: {
        Navbar,
    },
    data() {
        return {
            user: {
                username: "JohnDoe",
                email: "johndoe@example.com",
            },
        }
    },
};
</script>