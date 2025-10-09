const API_BASE_URL = 'http://127.0.0.1:5000';


function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const dateTimeString = now.toLocaleDateString('en-US', options);
    
    const element = document.getElementById('currentDateTime');
    if (element) {
        element.textContent = dateTimeString;
    }
}


function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    
    const icon = document.querySelector('.dark-mode-toggle i');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}


function loadDarkModePreference() {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        const icon = document.querySelector('.dark-mode-toggle i');
        if (icon) {
            icon.className = 'fas fa-sun';
        }
    }
}


function showNotification(message, type = 'success') {
    console.log(`[Notification] ${type.toUpperCase()}: ${message}`);
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '1100';
    notification.style.minWidth = '300px';
    notification.style.animation = 'fadeIn 0.3s ease';
    
    let icon = '';
    switch(type) {
        case 'success':
            icon = '<i class="fas fa-check-circle"></i>';
            break;
        case 'error':
        case 'danger':
            icon = '<i class="fas fa-exclamation-circle"></i>';
            break;
        case 'warning':
            icon = '<i class="fas fa-exclamation-triangle"></i>';
            break;
    }
    
    notification.innerHTML = `${icon} ${message}`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`[API Call] ${options.method || 'GET'} ${url}`);
    
    try {
        const response = await fetch(url, {
            ...options,
            mode: 'cors',
            credentials: 'omit'
        });
        
        console.log(`[API Response] Status: ${response.status}`);
        
        // Try to parse JSON
        let data;
        try {
            data = await response.json();
        } catch (e) {
            console.error('[API Error] Failed to parse JSON response:', e);
            throw new Error('Invalid response from server');
        }
        
        if (!response.ok) {
            console.error('[API Error]', data);
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        console.log('[API Success]', data);
        return data;
        
    } catch (error) {
        console.error('[API Error] Fetch failed:', error);
        
        // Check if it's a network error
        if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
            showNotification('Cannot connect to server. Please ensure the backend is running on http://127.0.0.1:5000', 'error');
        } else {
            showNotification(error.message, 'error');
        }
        
        throw error;
    }
}

function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Test API connection on page load
 */
async function testAPIConnection() {
    console.log('[Testing API Connection]');
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('[API Connection] Success:', data);
        return true;
    } catch (error) {
        console.error('[API Connection] Failed:', error);
        showNotification('⚠️ Cannot connect to backend server! Make sure it\'s running on http://127.0.0.1:5000', 'error');
        return false;
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Application] Initializing...');
    
    // Load dark mode preference
    loadDarkModePreference();
    
    // Start date/time update
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Test API connection
    testAPIConnection();
    
    console.log('[Application] Ready!');
});

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(20px);
        }
    }
`;
document.head.appendChild(style);
