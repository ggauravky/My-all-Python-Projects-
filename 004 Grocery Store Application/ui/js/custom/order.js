let productsData = [];
let orderItems = [];
let orderRowCounter = 0;


$(document).ready(function() {
    loadProducts();
    addOrderRow(); // Add first row by default
});

async function loadProducts() {
    try {
        productsData = await apiCall('/getProducts');
        console.log('Products loaded:', productsData.length);
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Failed to load products', 'error');
        productsData = [];
    }
}


function addOrderRow() {
    orderRowCounter++;
    
    // Create product options
    let productOptions = '<option value="">Select Product</option>';
    productsData.forEach(product => {
        productOptions += `<option value="${product.product_id}" data-price="${product.price_per_unit}" data-uom="${product.uom_name}">
            ${product.name} (${formatCurrency(product.price_per_unit)} / ${product.uom_name})
        </option>`;
    });
    
    const row = `
        <tr id="orderRow${orderRowCounter}">
            <td>
                <select class="form-control product-select" id="product${orderRowCounter}" onchange="calculateRowTotal(${orderRowCounter})">
                    ${productOptions}
                </select>
            </td>
            <td>
                <input type="number" 
                       class="form-control quantity-input" 
                       id="quantity${orderRowCounter}" 
                       placeholder="Qty" 
                       min="0.01" 
                       step="0.01"
                       value="1"
                       onchange="calculateRowTotal(${orderRowCounter})">
            </td>
            <td>
                <input type="text" 
                       class="form-control" 
                       id="price${orderRowCounter}" 
                       placeholder="Price" 
                       readonly>
            </td>
            <td>
                <input type="text" 
                       class="form-control" 
                       id="total${orderRowCounter}" 
                       placeholder="Total" 
                       readonly>
            </td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="removeOrderRow(${orderRowCounter})">
                    <i class="fas fa-times"></i>
                </button>
            </td>
        </tr>
    `;
    
    $('#orderTableBody').append(row);
}

/**
 * Remove an order row
 * @param {number} rowId - ID of the row to remove
 */
function removeOrderRow(rowId) {
    $(`#orderRow${rowId}`).remove();
    calculateGrandTotal();
}

/**
 * Calculate total for a specific row
 * @param {number} rowId - ID of the row to calculate
 */
function calculateRowTotal(rowId) {
    const productSelect = $(`#product${rowId}`);
    const quantity = parseFloat($(`#quantity${rowId}`).val()) || 0;
    
    if (productSelect.val() === '') {
        $(`#price${rowId}`).val('');
        $(`#total${rowId}`).val('');
        calculateGrandTotal();
        return;
    }
    
    const selectedOption = productSelect.find('option:selected');
    const price = parseFloat(selectedOption.data('price')) || 0;
    const total = price * quantity;
    
    $(`#price${rowId}`).val(formatCurrency(price));
    $(`#total${rowId}`).val(formatCurrency(total));
    
    calculateGrandTotal();
}

function calculateGrandTotal() {
    let grandTotal = 0;
    let itemCount = 0;
    
    $('.quantity-input').each(function() {
        const rowId = $(this).attr('id').replace('quantity', '');
        const total = parseFloat($(`#total${rowId}`).val().replace('₹', '')) || 0;
        
        if (total > 0) {
            grandTotal += total;
            itemCount++;
        }
    });
    
    $('#totalItems').text(itemCount);
    $('#grandTotal').text(formatCurrency(grandTotal));
}


async function submitOrder() {
    const customerName = $('#customerName').val().trim();
    
    // Validation
    if (!customerName) {
        showNotification('Please enter customer name', 'warning');
        $('#customerName').focus();
        return;
    }
    
    // Collect order items
    orderItems = [];
    let hasItems = false;
    
    $('.product-select').each(function() {
        const rowId = $(this).attr('id').replace('product', '');
        const productId = $(this).val();
        const quantity = parseFloat($(`#quantity${rowId}`).val()) || 0;
        const total = parseFloat($(`#total${rowId}`).val().replace('₹', '')) || 0;
        
        if (productId && quantity > 0) {
            hasItems = true;
            orderItems.push({
                product_id: productId,
                quantity: quantity,
                total_price: total
            });
        }
    });
    
    if (!hasItems) {
        showNotification('Please add at least one product to the order', 'warning');
        return;
    }
    
    // Calculate grand total
    const grandTotal = orderItems.reduce((sum, item) => sum + item.total_price, 0);
    
    // Prepare order data
    const orderData = {
        customer_name: customerName,
        grand_total: grandTotal,
        order_details: orderItems
    };
    
    try {
        const formData = new FormData();
        formData.append('data', JSON.stringify(orderData));
        
        const result = await apiCall('/insertOrder', {
            method: 'POST',
            body: formData
        });
        
        // Show success modal
        $('#orderIdDisplay').text(result.order_id);
        $('#customerNameDisplay').text(customerName);
        $('#totalAmountDisplay').text(formatCurrency(grandTotal));
        $('#successModal').modal('show');
        
        showNotification('Order placed successfully!', 'success');
        
    } catch (error) {
        console.error('Error submitting order:', error);
        showNotification('Failed to place order', 'error');
    }
}

function clearOrder() {
    if (!confirm('Are you sure you want to clear this order?')) {
        return;
    }
    
    $('#customerName').val('');
    $('#orderTableBody').empty();
    orderRowCounter = 0;
    addOrderRow();
    calculateGrandTotal();
    
    showNotification('Order cleared', 'success');
}


function newOrder() {
    $('#successModal').modal('hide');
    clearOrder();
}


function printOrder() {
    const orderId = $('#orderIdDisplay').text();
    const customerName = $('#customerNameDisplay').text();
    const totalAmount = $('#totalAmountDisplay').text();
    
    let printContent = `
        <html>
        <head>
            <title>Order #${orderId}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    text-align: center;
                    color: #2C3E50;
                }
                .order-info {
                    margin: 20px 0;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }
                th {
                    background-color: #4A90E2;
                    color: white;
                }
                .total {
                    font-size: 18px;
                    font-weight: bold;
                    text-align: right;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Grocery Store</h1>
            <h2>Order Receipt</h2>
            <div class="order-info">
                <p><strong>Order ID:</strong> ${orderId}</p>
                <p><strong>Customer:</strong> ${customerName}</p>
                <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    orderItems.forEach(item => {
        const product = productsData.find(p => p.product_id == item.product_id);
        if (product) {
            printContent += `
                <tr>
                    <td>${product.name}</td>
                    <td>${item.quantity} ${product.uom_name}</td>
                    <td>${formatCurrency(product.price_per_unit)}</td>
                    <td>${formatCurrency(item.total_price)}</td>
                </tr>
            `;
        }
    });
    
    printContent += `
                </tbody>
            </table>
            <div class="total">
                <p>Grand Total: ${totalAmount}</p>
            </div>
            <p style="text-align: center; margin-top: 40px;">Thank you for your business!</p>
        </body>
        </html>
    `;
    
    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.print();
}
