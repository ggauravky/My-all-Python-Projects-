let productsData = [];
let ordersData = [];


$(document).ready(function() {
    loadDashboardData();
});


async function loadDashboardData() {
    try {
        // Load products and orders in parallel
        await Promise.all([
            loadProducts(),
            loadOrders()
        ]);
        
        // Update dashboard statistics
        updateDashboardStats();
        
        // Display recent orders
        displayRecentOrders();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showNotification('Failed to load dashboard data', 'error');
    }
}


async function loadProducts() {
    try {
        productsData = await apiCall('/getProducts');
        console.log('Products loaded:', productsData.length);
    } catch (error) {
        console.error('Error loading products:', error);
        productsData = [];
    }
}


async function loadOrders() {
    try {
        ordersData = await apiCall('/getAllOrders');
        console.log('Orders loaded:', ordersData.length);
    } catch (error) {
        console.error('Error loading orders:', error);
        ordersData = [];
    }
}


function updateDashboardStats() {
    // Total Products
    $('#totalProducts').text(productsData.length);
    
    // Total Orders
    $('#totalOrders').text(ordersData.length);
    
    // Total Revenue
    const totalRevenue = ordersData.reduce((sum, order) => sum + parseFloat(order.total || 0), 0);
    $('#totalRevenue').text(formatCurrency(totalRevenue));
}


function displayRecentOrders() {
    const tableBody = $('#recentOrdersTable');
    tableBody.empty();
    
    if (ordersData.length === 0) {
        tableBody.html(`
            <tr>
                <td colspan="5" class="text-center">No orders found</td>
            </tr>
        `);
        return;
    }
    
    // Show only the 5 most recent orders
    const recentOrders = ordersData.slice(0, 5);
    
    recentOrders.forEach(order => {
        const row = `
            <tr>
                <td><strong>#${order.order_id}</strong></td>
                <td>${order.customer_name}</td>
                <td><strong>${formatCurrency(order.total)}</strong></td>
                <td>${formatDate(order.datetime)}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="viewOrderDetails(${order.order_id})">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteOrderFromDashboard(${order.order_id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tableBody.append(row);
    });
}

/**
 * View order details
 * @param {number} orderId - ID of the order to view
 */
async function viewOrderDetails(orderId) {
    try {
        const formData = new FormData();
        formData.append('order_id', orderId);
        
        const details = await apiCall('/getOrderDetails', {
            method: 'POST',
            body: formData
        });
        
        // Create modal to display order details
        let detailsHTML = `
            <div class="modal fade show" id="orderDetailsModal" style="display: block;">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-receipt"></i> Order #${orderId} Details
                            </h5>
                            <button type="button" class="close" onclick="closeModal('orderDetailsModal')">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Price/Unit</th>
                                        <th>Quantity</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
        `;
        
        let total = 0;
        details.forEach(item => {
            total += parseFloat(item.total_price);
            detailsHTML += `
                <tr>
                    <td>${item.product_name}</td>
                    <td>${formatCurrency(item.price_per_unit)} / ${item.uom_name}</td>
                    <td>${item.quantity} ${item.uom_name}</td>
                    <td><strong>${formatCurrency(item.total_price)}</strong></td>
                </tr>
            `;
        });
        
        detailsHTML += `
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <td colspan="3" style="text-align: right;"><strong>Grand Total:</strong></td>
                                        <td><strong style="color: var(--secondary-color); font-size: 18px;">${formatCurrency(total)}</strong></td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onclick="closeModal('orderDetailsModal')">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $('body').append(detailsHTML);
        
    } catch (error) {
        console.error('Error viewing order details:', error);
        showNotification('Failed to load order details', 'error');
    }
}

/**
 * Delete order from dashboard
 * @param {number} orderId - ID of the order to delete
 */
async function deleteOrderFromDashboard(orderId) {
    if (!confirm('Are you sure you want to delete this order?')) {
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('order_id', orderId);
        
        await apiCall('/deleteOrder', {
            method: 'POST',
            body: formData
        });
        
        showNotification('Order deleted successfully!', 'success');
        loadDashboardData(); // Reload data
        
    } catch (error) {
        console.error('Error deleting order:', error);
        showNotification('Failed to delete order', 'error');
    }
}

/**
 * Close modal
 * @param {string} modalId - ID of the modal to close
 */
function closeModal(modalId) {
    $(`#${modalId}`).remove();
}
