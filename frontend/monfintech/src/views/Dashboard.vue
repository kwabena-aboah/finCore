<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Welcome to MonFintech Dashboard</h1>
            <p>Manage your financial transactions, budget, and more!</p>

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                @click="openModal()"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

            <!-- Payment Modal -->
            <div class="modal" tabindex="-1" ref="paymentModal" id="paymentModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Make a Payment</h5>
                            <button type="button" class="btn-close" @click="closeModal()"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="submitPayment">
                                <div class="mb-3">
                                    <label class="form-label" for="amount">Amount</label>
                                    <input type="number" name="amount" class="form-control" v-model="payment.amount" required="">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" for="payment_method">Payment Method</label>
                                    <select class="form-select" v-model="payment.payment_method" required="">
                                        <option value="" disabled="">Select Payment Method</option>
                                        <option value="crypto">Cryptocurrency</option>
                                        <option value="card">Credit/Debit Card</option>
                                        <option value="mobile_money">Mobile Money</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" for="recipient">Recipient</label>
                                    <input type="text" name="recipient" class="form-control" v-model="payment.recipient" required="">
                                </div>
                                <button class="btn btn-primary" type="submit">Submit</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
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
    data() {
        return {
            payment: {
                amount: null,
                payment_method: '',
                recipient: '',
            },
        };
    },
    created() {
        toast.success("Login successful!", {
          autoClose: 8000,
        });
    },
    methods: {
        openModal() {
            this.$refs.paymentModal.style.display = 'block';
        },
        closeModal() {
            this.$refs.paymentModal.style.display = 'none';
        },
        async submitPayment() {
            try {
                const response = await instance.post('payments/', this.payment, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                toast.success("Payment Successful:", response.data);
                this.closeModal();
            } catch (error) {
                toast.error("Payment Failed:", error.response.data);
            }
        },
    },
};
</script>
<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>