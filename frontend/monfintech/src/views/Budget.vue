<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h2 class="text-center">Budgets</h2>

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                @click="openModal('create')"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

            <!-- Add Budget Modal -->
             <div class="modal fade" id="budgetModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="budgetModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="budgetModalLabel">{{ modalTitle }}</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="handleSubmit">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="budget_name" class="form-label">Budget Name</label>
                                    <input type="text" id="budget_name" v-model="form.budget_name" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="amount" class="form-label">Amount</label>
                                    <input type="number" id="amount" v-model="form.amount" class="form-control" required />
                                </div>
                                <div v-if="errors" class="alert alert-danger">
                                    <p v-for="(error, field) in errors" :key="field">{{ field }}: {{ error }}</p>
                                </div>
                                <div class="mb-3">
                                    <label for="description" class="form-label">Description</label>
                                    <textarea name="description" id="description" rows="3" v-model="form.description" class="form-control" required></textarea>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary">{{ modalAction }}</button>
                            </div>
                        </form>
                    </div>
                </div>
             </div>

             <!-- Search filter -->
             <div class="mb-3">
                 <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search budgets..." @input="fetchBudgets(1)">
             </div>

            <!-- Budget list -->
              <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Budget Name</th>
                        <th>Amount</th>
                        <th>Description</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody v-if="this.budgets?.length > 0">
                    <tr v-for="budget in budgets" :key="budget.id">
                        <td>{{ budget.budget_name }}</td>
                        <td>{{ budget.amount }}</td>
                        <td>{{ budget.description }}</td>
                        <td>{{ budget.updated_at }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', budget)">Edit</button>
                            <button class="btn btn-sm btn-danger" @click="deleteBudget(budget.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="5">Loading...</td>
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
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { Modal } from "bootstrap";
import Navbar from '@/components/Navbar.vue';
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: "BudgetPage",
    data() {
        return {
            budgets: [],
            form: {
                id: null,
                budget_name: "",
                amount: "",
                description: "",
            },
            searchQuery: "",
            errors: null,
            page: 1,
            modalTitle: '',
            modalAction: '',
            pagination: {
                next: null,
                prev: null,
            },
        };
    },
    methods: {
        async fetchBudgets(url = `budgets/?q=${this.searchQuery}&page=${this.page}`) {
            try {
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.budgets = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching budgets!");
                console.error("Error fetching budgets:", error);
            }
        },
        openModal(action, budget = null) {
            if (action === 'create') {
                this.modalTitle = 'Add Budget';
                this.modalAction = 'Create';
                this.form = { id: null, budget_name: '', amount: '', description: '' };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Budget';
                this.modalAction = 'Update';
                this.form = { ...budget };
            }
            const modal = new Modal(document.getElementById('budgetModal'));
            modal.show();
        },
        handleSubmit() {
            // const action = this.modalAction === 'Create' ? this.createBudget : this.updateBudget;
            // action().catch(err => {
            //     this.errors = err.response.data;
            // });
            if (this.modalAction === 'Create') {
                this.createBudget();
            } else {
                this.updateBudget();
            }
        },
        async createBudget() {
            try {
                const response = await instance.post("budgets/", this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.budgets = response.data; // Add new budget to the  list
                toast.success("Budget created successfully!");
                this.fetchBudgets();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding budget:", error);
                toast.error("Failed to create budget.", error);
            }
        },
        async updateBudget() {
            try {
                const response = await instance.put(`budgets/${this.form.id}/`, this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'application/json',
                    }
                });
                this.budgets = response.data;
                toast.success("Budget updated successfully!");
                this.fetchBudgets();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating budget!", error);
                // console.error("Error updating budget:", error);
            }
        },
        async deleteBudget(id) {
            if(confirm('Are you sure you want to delete this budget?')){
                await instance.delete(`budgets/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => this.fetchBudgets(), toast.success("Budget deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting budget!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('budgetModal'));
            modal.hide();
        },
    },
    created() {
        this.fetchBudgets();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>