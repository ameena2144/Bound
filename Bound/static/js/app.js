// Legal Case Binder - Application JavaScript
// Handles client-side interactions and enhancements

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize file upload handlers
    initializeFileUpload();
    
    // Initialize timeline filtering
    initializeTimelineFilters();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize auto-save for forms
    initializeAutoSave();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Initialize date/time helpers
    initializeDateTimeHelpers();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time validation feedback
    const inputs = document.querySelectorAll('input[required], textarea[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}

/**
 * Validate individual form field
 */
function validateField(field) {
    const isValid = field.checkValidity();
    
    field.classList.remove('is-valid', 'is-invalid');
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Show custom validation messages
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback && !isValid) {
        if (field.validity.valueMissing) {
            feedback.textContent = `${field.labels[0]?.textContent || 'This field'} is required.`;
        } else if (field.validity.typeMismatch) {
            feedback.textContent = `Please enter a valid ${field.type}.`;
        } else if (field.validity.tooShort) {
            feedback.textContent = `Please enter at least ${field.minLength} characters.`;
        }
    }
}

/**
 * Initialize file upload functionality
 */
function initializeFileUpload() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        
        if (!fileInput) return;
        
        // Drag and drop handlers
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelection(fileInput);
            }
        });
        
        // Click to select file
        area.addEventListener('click', () => {
            fileInput.click();
        });
        
        // File selection handler
        fileInput.addEventListener('change', () => {
            handleFileSelection(fileInput);
        });
    });
}

/**
 * Handle file selection and preview
 */
function handleFileSelection(input) {
    const file = input.files[0];
    if (!file) return;
    
    const uploadArea = input.closest('.upload-area');
    if (!uploadArea) return;
    
    // Show file info
    const fileName = file.name;
    const fileSize = formatFileSize(file.size);
    const fileType = file.type || 'Unknown';
    
    let preview = uploadArea.querySelector('.file-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'file-preview mt-3';
        uploadArea.appendChild(preview);
    }
    
    preview.innerHTML = `
        <div class="d-flex align-items-center">
            <i data-feather="file" class="me-2"></i>
            <div>
                <div class="fw-medium">${fileName}</div>
                <small class="text-muted">${fileSize} • ${fileType}</small>
            </div>
        </div>
    `;
    
    // Re-initialize feather icons for the new element
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * Initialize timeline filtering
 */
function initializeTimelineFilters() {
    const filterButtons = document.querySelectorAll('[onclick^="filterTimeline"]');
    
    // Add click handlers for timeline filters
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const type = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            filterTimeline(type);
        });
    });
}

/**
 * Filter timeline events by type
 */
function filterTimeline(type) {
    const timelineItems = document.querySelectorAll('.timeline-item');
    const filterButtons = document.querySelectorAll('[onclick^="filterTimeline"]');
    
    // Update button states
    filterButtons.forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    });
    
    // Highlight active filter
    const activeButton = document.querySelector(`[onclick="filterTimeline('${type}')"]`);
    if (activeButton) {
        activeButton.classList.remove('btn-outline-primary');
        activeButton.classList.add('btn-primary');
    }
    
    // Filter timeline items
    timelineItems.forEach(item => {
        const itemType = item.getAttribute('data-event-type');
        
        if (type === 'all' || itemType === type) {
            item.style.display = 'block';
            item.classList.add('fade-in');
        } else {
            item.style.display = 'none';
            item.classList.remove('fade-in');
        }
    });
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    
    searchInputs.forEach(input => {
        const targetSelector = input.getAttribute('data-search');
        
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targets = document.querySelectorAll(targetSelector);
            
            targets.forEach(target => {
                const text = target.textContent.toLowerCase();
                const matches = text.includes(searchTerm);
                
                target.style.display = matches || searchTerm === '' ? 'block' : 'none';
                
                if (matches && searchTerm !== '') {
                    highlightSearchTerm(target, searchTerm);
                } else {
                    removeHighlight(target);
                }
            });
        });
    });
}

/**
 * Highlight search terms
 */
function highlightSearchTerm(element, term) {
    const originalText = element.textContent;
    const regex = new RegExp(`(${term})`, 'gi');
    const highlightedText = originalText.replace(regex, '<mark>$1</mark>');
    
    // Store original text if not already stored
    if (!element.hasAttribute('data-original-text')) {
        element.setAttribute('data-original-text', originalText);
    }
    
    element.innerHTML = highlightedText;
}

/**
 * Remove search highlighting
 */
function removeHighlight(element) {
    const originalText = element.getAttribute('data-original-text');
    if (originalText) {
        element.textContent = originalText;
        element.removeAttribute('data-original-text');
    }
}

/**
 * Initialize auto-save functionality for forms
 */
function initializeAutoSave() {
    const forms = document.querySelectorAll('[data-autosave]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                saveFormData(form);
            });
        });
        
        // Load saved data on page load
        loadFormData(form);
    });
}

/**
 * Save form data to localStorage
 */
function saveFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    const formId = form.id || form.getAttribute('data-autosave');
    localStorage.setItem(`form-${formId}`, JSON.stringify(data));
    
    // Show save indicator
    showSaveIndicator();
}

/**
 * Load form data from localStorage
 */
function loadFormData(form) {
    const formId = form.id || form.getAttribute('data-autosave');
    const savedData = localStorage.getItem(`form-${formId}`);
    
    if (savedData) {
        const data = JSON.parse(savedData);
        
        Object.entries(data).forEach(([key, value]) => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && !field.value) { // Only set if field is empty
                field.value = value;
            }
        });
    }
}

/**
 * Show save indicator
 */
function showSaveIndicator() {
    let indicator = document.querySelector('.save-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'save-indicator position-fixed top-0 end-0 m-3 alert alert-success alert-dismissible fade';
        indicator.innerHTML = `
            <i data-feather="check-circle" class="me-2"></i>
            Changes saved automatically
        `;
        document.body.appendChild(indicator);
    }
    
    indicator.classList.add('show');
    
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 2000);
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save forms
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const activeForm = document.activeElement.closest('form');
            if (activeForm) {
                activeForm.requestSubmit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
        
        // Ctrl/Cmd + / to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[data-search]');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
}

/**
 * Initialize date/time helpers
 */
function initializeDateTimeHelpers() {
    // Set default datetime-local values to current time
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]:not([value])');
    datetimeInputs.forEach(input => {
        if (!input.value && input.hasAttribute('data-default-now')) {
            const now = new Date();
            now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
            input.value = now.toISOString().slice(0, 16);
        }
    });
    
    // Add relative time displays
    const timeElements = document.querySelectorAll('[data-timestamp]');
    timeElements.forEach(element => {
        const timestamp = element.getAttribute('data-timestamp');
        const relativeTime = getRelativeTime(new Date(timestamp));
        
        // Add relative time as a tooltip or subtitle
        if (element.hasAttribute('title')) {
            element.setAttribute('title', element.getAttribute('title') + ' (' + relativeTime + ')');
        } else {
            const small = document.createElement('small');
            small.className = 'text-muted ms-2';
            small.textContent = '(' + relativeTime + ')';
            element.appendChild(small);
        }
    });
}

/**
 * Get relative time string
 */
function getRelativeTime(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMinutes < 1) return 'just now';
    if (diffMinutes < 60) return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) !== 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString();
}

/**
 * Utility functions
 */

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-legal mx-auto';
    spinner.setAttribute('data-loading-spinner', 'true');
    
    const originalContent = element.innerHTML;
    element.setAttribute('data-original-content', originalContent);
    element.innerHTML = '';
    element.appendChild(spinner);
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(element) {
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
        element.disabled = false;
    }
}

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Copied to clipboard', 'success');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Format dates consistently
function formatDate(date, includeTime = false) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    
    if (includeTime) {
        options.hour = 'numeric';
        options.minute = '2-digit';
        options.hour12 = true;
    }
    
    return new Intl.DateTimeFormat('en-US', options).format(new Date(date));
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate phone format
function isValidPhone(phone) {
    const phoneRegex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    return phoneRegex.test(phone);
}
