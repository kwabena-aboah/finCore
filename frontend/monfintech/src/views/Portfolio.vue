<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div class="container mt-5">
                <h2 class="text-center">Asset Prices by Market Cap</h2>

                <!-- Search and Add Button -->
                <div class="d-flex justify-content-between mb-3">
                    <input 
                        type="text" 
                        name="search"
                        class="form-control w-50"
                        v-model="searchQuery"
                        placeholder="Search by symbol or type"
                        @input="fetchAssets(1)"
                        />
                    <button class="btn btn-primary" @click="openModal('create')">Add Asset</button>
                </div>

                <!-- Asset Table -->
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Asset Type</th>
                            <th>Symbol</th>
                            <th>Quantity</th>
                            <th>Purchase Price</th>
                            <th>Current Price (USD)</th>
                            <th>Current Value (USD)</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="asset in assets" :key="asset.id">
                            <td>{{ asset.asset_type }}</td>
                            <td>{{ asset.symbol }}</td>
                            <td>{{ asset.quantity }}</td>
                            <td>{{ asset.purchase_price || '-'}}</td>
                            <td>
                                <span v-if="asset.current_price !== undefined">{{ asset.current_price }}</span>
                                <span v-else>Loading...</span>
                            </td>
                            <td>
                                <span v-if="asset.current_price !== undefined">
                                    {{ (asset.current_price * asset.quantity).toFixed(2) }}
                                </span>
                                <span v-else>-</span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', asset)">Edit</button> | 
                                <button class="btn btn-sm btn-danger" @click="deleteAsset(asset.id)">Delete</button> | 
                                <button class="btn btn-sm btn-info" @click="refreshPrice(asset)">Refresh Price</button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <!-- Pagination Controls -->
                <nav aria-label="Page navigation">
                    <ul class="pagination justify-content-center">
                        <li class="page-item" :class="{ disabled: currentPage === 1}">
                            <a class="page-link" href="#" @click.prevent="fetchAssets(currentPage - 1)">Previous</a>
                        </li>
                        <li class="page-item disabled">
                            <span class="page-link">{{ currentPage }} / {{ totalPages }}</span>
                        </li>
                        <li class="page-item" :class="{ disabled: currentPage === totalPages}">
                            <a class="page-link" href="#" @click.prevent="fetchAssets(currentPage + 1)">Next</a>
                        </li>
                    </ul>
                </nav>

                <!-- Asset Modal -->
                <div class="modal fade" id="assetModal" tabindex="-1" aria-hidden="true" ref="assetModal">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">{{ modalTitle }}</h5>
                                <button type="button" class="btn-close" @click="closeModal()"></button>
                            </div>
                            <div class="modal-body">
                                <form @submit.prevent="handleSubmit">
                                    <div class="mb-3">
                                        <label class="form-label">Asset Type</label>
                                        <select class="form-select" v-model="form.asset_type" required>
                                            <option value="stock">Stock</option>
                                            <option value="crypto">Cryptocurrency</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Symbol</label>
                                        <input type="text" name="symbol" class="form-control" v-model="form.symbol" required />
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Quantity</label>
                                        <input type="number" name="quantity" class="form-control" v-model="form.quantity" required />
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Purchase Price</label>
                                        <input type="number" name="purchase_price" class="form-control" v-model="form.purchase_price" required />
                                    </div>
                                    <button type="submit" class="btn btn-primary">{{ modalAction }}</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { Modal } from "bootstrap";
import Navbar from "@/components/Navbar.vue"
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: 'PortfolioPage',
    data() {
        return {
            assets: [],
            searchQuery: "",
            currentPage: 1,
            totalPages: 1,
            // Form data for creating or editing an asset
            form: {
                id: null,
                asset_type: "stock",
                symbol: "",
                quantity: null,
                purchase_price: null,
            },
            modalTitle: "",
            modalAction: "",
        };
    },
    methods: {
        fetchAssets(page = 1) {
            // Fetch assets with pagination and search filtering
            instance.get(`assets/?page=${page}&search=${this.searchQuery}`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
            })
            .then((response) => {
                this.assets = response.data.results;
                this.currentPage = page;
                const total = response.data.count;
                this.totalPages = Math.ceil(total / 10);
                // For each asset fetch current price
                this.assets.forEach((asset) => {
                    this.fetchCurrentPrice(asset);
                });
            })
            .catch((error) => {
                console.error("Error fetching assets:", error);
                toast.error("Error fetching assets:", error);
            });
        },
        fetchCurrentPrice(asset) {
            instance.get(`assets/${asset.id}/price/`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
            })
            .then((response) => {
                asset.current_price = parseFloat(response.data.price);
            })
            .catch((error) => {
                console.error(`Error fetching price for ${asset.symbol}:`, error);
                toast.error(`Error fetching price for ${asset.symbol}:`, error);
                asset.current_price = 0;
            });
        },
        refreshPrice(asset) {
            this.fetchCurrentPrice(asset);
        },
        openModal(action, asset = null) {
            if (action === "create") {
                this.modalTitle = "Add Asset";
                this.modalAction = "Create";
                this.form = {
                    id: null,
                    asset_type: "stock",
                    symbol: "",
                    quantity: null,
                    purchase_price: null,
                };
            } else if (action === "edit" && asset){
                this.modalTitle = "Edit Asset";
                this.modalAction = "Update";
                this.form = { ...asset };
            }
            // Show modal
            const modalEl = document.getElementById("assetModal");
            const modalInstance = new Modal(modalEl);
            modalInstance.show();
        },
        closeModal() {
            const modalEl = document.getElementById("assetModal");
            const modalInstance = Modal.getInstance(modalEl);
            if (modalInstance) modalInstance.hide();
        },
        handleSubmit() {
            if (this.modalAction === "Create") {
                this.createAsset();
            } else {
                this.updateAsset();
            }
        },
        createAsset(){
            instance.post("assets/", this.form, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
            }).then(() => {
                this.fetchAssets(this.currentPage);
                this.closeModal();
                toast.success("Asset added successfully");
            })
            .catch(error => {
                console.error("Error creating asset:", error.response.data);
                toast.error("Failed to create asset", error.response.data);
            })
        },
        updateAsset() {
            instance.put(`assets/${this.form.id}/`, this.form, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
            })
            .then(() => {
                this.fetchAssets(this.currentPage);
                this.closeModal();
                toast.success("Asset updated successfully");
            })
            .catch(error => {
                console.error("Error updating asset:", error.response.data);
                toast.error("Failed to update asset", error.response.data);
            })
        },
        deleteAsset(assetId) {
            if(confirm("Are you sure you want to delete this asset?")) {
                instance.delete(`assets/${assetId}/`, {
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => {
                    this.fetchAssets(this.currentPage);
                    toast.success("Asset deleted successfully");
                })
                .catch(error => {
                    console.error("Error deleting asset:", error.response.data);
                    toast.error("Failed to delete asset", error.response.data)
                });
            }
        },
    },
    mounted() {
        this.fetchAssets();
    },
};
</script>
<style scoped>
    .table {
        margin-top: 20px;
    }
</style>