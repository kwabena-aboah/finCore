<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h2 class="text-center">User Profile</h2>
            <div class="card shadow-sm p-4" v-if="profile">
                <form @submit.prevent="updateProfile">
                    <div class="mb-3">
                        <label for="bio" class="form-label">Bio</label>
                        <textarea name="bio" id="bio" rows="3" v-model="profile.bio" class="form-control" placeholder="Tell us about yourself"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone</label>
                        <input type="text" name="phone" id="phone" v-model="profile.phone" class="form-control" placeholder="Enter your phone number" />
                    </div>
                    <button type="submit" class="btn btn-primary">Update Profile</button>
                </form>
            </div>
            <div v-else>
                <p class="text-center">Loading profile...</p>
            </div>
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import Navbar from '@/components/Navbar.vue';
import Sidebar from "@/components/Sidebar.vue"

export default {
    name: "ProfilePage",
    components: {
        Navbar,
        Sidebar,
    },
    data() {
        return {
            profile: null,
        }
    },
    created() {
        this.fetchUserDetails();
    },
    methods: {
        async fetchUserDetails(url="auth/profile/"){
            try {
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.profile = response.data;
                console.log(response.data);
            } catch (error) {
                console.error("Error fetching user profile:", error);
            }
        },
        async updateProfile(url="auth/profile/") {
            try {
                const response = await instance.put(url, this.profile, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.profile = response.data
                if (response.status === 200) {
                    console.log('Profile updated successfully:', response.data);
                } else {
                    console.log("Unexpected response:", response);
                }
                console.log(response.data)
            } catch (error) {
                console.error("Error updating profile:", error.response ? error.response.data : error.message);
            }
        },
    },
};
</script>

<style scoped>
.card {
    max-width: 600px;
    margin: 0 auto;
}
</style>