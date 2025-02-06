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
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

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
        async updateProfile() {
            try {
                const response = await instance.put("auth/profile/", this.profile, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'application/json',
                }
                });
                if (response.status === 200) {
                    this.profile = response.data
                    toast.success("Profile updated successfully");
                    // alert("Profile updated successfully")
                    // console.log('Profile updated successfully:', response.data);
                } else {
                    toast.warn("Unexpected response");
                    // alert("Unexpected response")
                    // console.log("Unexpected response:", response);
                }
                console.log(response.data)
            } catch (error) {
                toast.error("Error updating profile:", error.response ? error.response.data : error.message);
                // console.error("Error updating profile:", error.response ? error.response.data : error.message);
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