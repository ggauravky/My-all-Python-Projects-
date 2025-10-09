
let productsData = [];
let uomData = [];
let editingProductId = null;


$(document).ready(function() {
    loadUOM();
    loadProducts();
    
    // Handle form submission
    $('#productForm').on('submit', function(e) {
        e.preventDefault();
        saveProduct();
    });
});


async function loadUOM() {
    try {
        uomData = await apiCall('/getUOM');
        
        // Populate UOM dropdown
        const select = $('#productUnit');
        select.empty();
        select.append('<option value="">Select Unit</option>');
        
        uomData.forEach(uom => {
            select.append(`<option value="${uom.uom_id}">${uom.uom_name}</option>`);
        });
        
    } catch (error) {
        console.error('Error loading UOM:', error);
        showNotification('Failed to load units of measurement', 'error');
    }
}


async function loadProducts() {
    try {
        productsData = await apiCall('/getProducts');
        displayProducts();
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Failed to load products', 'error');
    }
}

/**
 * Display products in table
 */
function displayProducts() {
    const tableBody = $('#productTableBody');
    tableBody.empty();
    
    if (productsData.length === 0) {
        tableBody.html(`
            <tr>
                <td colspan="5" class="text-center">No products found. Add your first product!</td>
            </tr>
        `);
        return;
    }
    
    productsData.forEach(product => {
        const row = `
            <tr>
                <td>${product.product_id}</td>
                <td><strong>${product.name}</strong></td>
                <td><span class="badge badge-success">${product.uom_name}</span></td>
                <td><strong>${formatCurrency(product.price_per_unit)}</strong></td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-warning" onclick="editProduct(${product.product_id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="confirmDelete(${product.product_id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </td>
            </tr>
        `;
        tableBody.append(row);
    });
}

/**
 * Save product (add new or update existing)
 */
async function saveProduct() {
    const productName = $('#productName').val().trim();
    const uomId = $('#productUnit').val();
    const pricePerUnit = $('#productPrice').val();
    
    // Validation
    if (!productName || !uomId || !pricePerUnit) {
        showNotification('Please fill all required fields', 'warning');
        return;
    }
    
    if (parseFloat(pricePerUnit) <= 0) {
        showNotification('Price must be greater than 0', 'warning');
        return;
    }
    
    try {
        const formData = new FormData();
        
        const productData = {
            product_name: productName,
            uom_id: uomId,
            price_per_unit: pricePerUnit
        };
        
        if (editingProductId) {
            // Update existing product
            productData.product_id = editingProductId;
            formData.append('data', JSON.stringify(productData));
            
            await apiCall('/updateProduct', {
                method: 'POST',
                body: formData
            });
            
            showNotification('Product updated successfully!', 'success');
            editingProductId = null;
            
        } else {
            // Add new product
            formData.append('data', JSON.stringify(productData));
            
            await apiCall('/insertProduct', {
                method: 'POST',
                body: formData
            });
            
            showNotification('Product added successfully!', 'success');
        }
        
        // Reset form and reload products
        resetForm();
        loadProducts();
        
    } catch (error) {
        console.error('Error saving product:', error);
        showNotification('Failed to save product', 'error');
    }
}

/**
 * Edit product
 * @param {number} productId - ID of product to edit
 */
function editProduct(productId) {
    const product = productsData.find(p => p.product_id === productId);
    
    if (!product) {
        showNotification('Product not found', 'error');
        return;
    }
    
    // Fill form with product data
    $('#productId').val(product.product_id);
    $('#productName').val(product.name);
    $('#productUnit').val(product.uom_id);
    $('#productPrice').val(product.price_per_unit);
    
    // Update form title
    $('#formTitle').text('Edit Product');
    
    // Store editing product ID
    editingProductId = productId;
    
    // Scroll to form
    $('html, body').animate({
        scrollTop: $('#productForm').offset().top - 100
    }, 500);
}

/**
 * Show delete confirmation modal
 * @param {number} productId - ID of product to delete
 */
function confirmDelete(productId) {
    editingProductId = productId;
    $('#deleteModal').modal('show');
    
    // Handle delete confirmation
    $('#confirmDelete').off('click').on('click', function() {
        deleteProduct();
    });
}


async function deleteProduct() {
    try {
        const formData = new FormData();
        formData.append('product_id', editingProductId);
        
        await apiCall('/deleteProduct', {
            method: 'POST',
            body: formData
        });
        
        showNotification('Product deleted successfully!', 'success');
        $('#deleteModal').modal('hide');
        editingProductId = null;
        loadProducts();
        
    } catch (error) {
        console.error('Error deleting product:', error);
        showNotification('Failed to delete product', 'error');
    }
}


function resetForm() {
    $('#productForm')[0].reset();
    $('#productId').val('');
    $('#formTitle').text('Add New Product');
    editingProductId = null;
}


function filterProducts() {
    const searchTerm = $('#searchProduct').val().toLowerCase();
    
    $('#productTableBody tr').each(function() {
        const productName = $(this).find('td:eq(1)').text().toLowerCase();
        
        if (productName.includes(searchTerm)) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}
