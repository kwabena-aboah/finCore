<template>
    <div>
        <Navbar />
        <div class="container mt-5">
            <h2 class="text-center">Transactions</h2>

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                data-bs-toggle="modal"
                data-bs-target="#addTransactionModal"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

            <!-- Add Transaction Modal -->
             <div class="modal fade" id="addTransactionModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="addTransactionModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="addTransactionModalLabel">Add Transaction</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="addTransaction">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="amount" class="form-label">Amount</label>
                                    <input type="number" id="amount" v-model="newTransaction.amount" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="category" class="form-label">Category</label>
                                    <select name="category" id="category" v-model="newTransaction.category" class="form-select" required>
                                        <option value="" disabled>Select Category</option>
                                        <option value="INCOME">Income</option>
                                        <option value="EXPENSE">Expense</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label for="description" class="form-label">Description</label>
                                    <textarea name="description" id="description" rows="3" v-model="newTransaction.description" class="form-control" required></textarea>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary">Add Transaction</button>
                            </div>
                        </form>
                    </div>
                </div>
             </div>

            <!-- Filter Section -->
             <form @submit.prevent="fetchTransactions" class="mb-4">
                <div class="row g-3 align-items-end">
                    <div class="col-md-3">
                        <select name="category" id="category" v-model="filters.category" class="form-control">
                            <option value="" disabled>Filter by Category</option>
                            <option value="INCOME">Income</option>
                            <option value="EXPENSE">Expense</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <input 
                            type="date"
                            class="form-control"
                            placeholder="Filter by Date"
                            v-model="filters.date"
                            />
                    </div>
                    <div class="col-md-2">
                        <button type="submit" class="btn btn-primary w-100">Apply Filters</button>
                    </div>
                </div>
             </form>

             <!-- Transaction list -->
              <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Category</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody v-if="this.transactions?.length > 0">
                    <tr v-for="transaction in transactions" :key="transaction.id">
                        <td>{{ transaction.date }}</td>
                        <td>{{ transaction.amount }}</td>
                        <td>{{ transaction.category }}</td>
                        <td>{{ transaction.description || '-' }}</td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="4">Loading...</td>
                    </tr>
                </tbody>
              </table>

              <!-- Pagination controls -->
               <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.prev }"
                        @click="changePage(pagination.prev)">
                        <a href="#" class="page-link">Previous</a>
                    </li>
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.next }"
                        @click="changePage(pagination.next)">
                        <a href="#" class="page-link">Next</a>
                    </li>
                </ul>
               </nav>
        </div>
    </div>
</template>

<script>
import instance from '@/api/axios';
// import { Modal } from "bootstrap";
import Navbar from '@/components/Navbar.vue';

export default {
    components: {
        Navbar,
    },
    name: "TransactionsPage",
    data() {
        return {
            transactions: [],
            newTransaction: {
                amount: "",
                category: "",
                description: "",
            },
            filters: {
                category: "",
                date: "",
            },
            pagination: {
                next: null,
                prev: null,
            },
        };
    },
    methods: {
        async fetchTransactions(url = "transactions/") {
            try {
                const params = {
                    category: this.filters.category,
                    date: this.filters.date,
                };
                const response = await instance.get(url, { params }, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.transactions = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                console.error("Error fetching transactions:", error);
            }
        },
        changePage(url) {
            if (url) {
                this.fetchTransactions(url);
            }
        },
        async addTransaction() {
            try {
                const response = await instance.post("transactions/", this.newTransaction, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.transactions.unshift(response.data); // Add new transactions to the  list
                this.newTransaction = { amount: "", category: "", description: "" };    // Reset form
                // const modal = document.getElementById("addTransactionModal");
                // const bootstrapModal = Modal.getInstance(modal);
                // bootstrapModal.hide(); // Close modal
                // if (modal) {
                //     bootstrapModal.hide(); // Close modal
                // }
            } catch (error) {
                console.error("Error adding transaction:", error);
            }
        },
    },
    created() {
        this.fetchTransactions();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>