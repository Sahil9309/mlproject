// Main JavaScript for Student Performance Predictor

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Initialize animations
    initializeAnimations();
});

// Form Validation
function initializeFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearValidation);
    });
    
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showAlert('Please fill in all required fields correctly.', 'danger');
        } else {
            showLoadingState();
        }
    });
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Remove existing feedback
    const existingFeedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    let isValid = true;
    let message = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    
    // Specific field validations
    if (value) {
        switch (field.type) {
            case 'number':
                const num = parseFloat(value);
                const min = parseFloat(field.min);
                const max = parseFloat(field.max);
                
                if (isNaN(num)) {
                    isValid = false;
                    message = 'Please enter a valid number.';
                } else if (min !== undefined && num < min) {
                    isValid = false;
                    message = `Value must be at least ${min}.`;
                } else if (max !== undefined && num > max) {
                    isValid = false;
                    message = `Value must be at most ${max}.`;
                }
                break;
        }
    }
    
    // Apply validation styling
    if (isValid && value) {
        field.classList.add('is-valid');
        showFieldFeedback(field, 'Looks good!', 'valid');
    } else if (!isValid) {
        field.classList.add('is-invalid');
        showFieldFeedback(field, message, 'invalid');
    }
    
    return isValid;
}

function clearValidation(e) {
    const field = e.target;
    field.classList.remove('is-valid', 'is-invalid');
    
    const feedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

function showFieldFeedback(field, message, type) {
    const feedback = document.createElement('div');
    feedback.className = `${type}-feedback`;
    feedback.textContent = message;
    field.parentNode.appendChild(feedback);
}

function validateForm() {
    const form = document.getElementById('predictionForm');
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField({ target: field })) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Interactive Elements
function initializeInteractiveElements() {
    // Score input sliders (if any)
    const scoreInputs = document.querySelectorAll('input[type="number"]');
    scoreInputs.forEach(input => {
        input.addEventListener('input', function() {
            updateScoreDisplay(this);
        });
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        });
    }, 5000);
}

function updateScoreDisplay(input) {
    const value = input.value;
    const label = input.previousElementSibling;
    
    if (label && label.tagName === 'LABEL') {
        const originalText = label.textContent.split('(')[0].trim();
        if (value) {
            label.innerHTML = `${originalText} <span class="badge bg-primary">${value}</span>`;
        } else {
            label.textContent = originalText;
        }
    }
}

// Animations
function initializeAnimations() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements with animation class
    const animatedElements = document.querySelectorAll('.feature-card, .stat-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Loading State
function showLoadingState() {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading"></span> Predicting...';
        submitBtn.disabled = true;
        
        // Re-enable after 10 seconds (fallback)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 10000);
    }
}

// Alert System
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertContainer.remove();
        }, 5000);
    }
}

// Utility Functions
function formatScore(score) {
    return Math.round(score * 100) / 100;
}

function getScoreCategory(score) {
    if (score >= 80) return { category: 'Excellent', class: 'success', icon: 'fas fa-star' };
    if (score >= 70) return { category: 'Good', class: 'info', icon: 'fas fa-thumbs-up' };
    if (score >= 60) return { category: 'Average', class: 'warning', icon: 'fas fa-exclamation-triangle' };
    return { category: 'Below Average', class: 'danger', icon: 'fas fa-exclamation-circle' };
}

// Form Auto-save (optional)
function initializeAutoSave() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        // Load saved value
        const savedValue = localStorage.getItem(`form_${input.name}`);
        if (savedValue && input.type !== 'submit') {
            input.value = savedValue;
        }
        
        // Save on change
        input.addEventListener('change', function() {
            localStorage.setItem(`form_${this.name}`, this.value);
        });
    });
}

// Clear saved form data
function clearSavedFormData() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        localStorage.removeItem(`form_${input.name}`);
    });
}

// Export functions for global use
window.StudentPredictor = {
    showAlert,
    formatScore,
    getScoreCategory,
    clearSavedFormData
};