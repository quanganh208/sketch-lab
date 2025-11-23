/**
 * SketchLab - Main JavaScript
 * Handles UI interactions and processing logic
 */

// Global state (accessible from upload.js too)
window.uploadedFilename = null;

// DOM Elements
const processBtn = document.getElementById('process-btn');
const loadingDiv = document.getElementById('loading');
const messageDiv = document.getElementById('message');
const algorithmSelect = document.getElementById('algorithm');

/**
 * Initialize app when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('SketchLab initialized');

    // Setup process button click handler
    if (processBtn) {
        processBtn.addEventListener('click', processImage);
    }

    // Setup algorithm change handler for descriptions
    if (algorithmSelect) {
        algorithmSelect.addEventListener('change', function() {
            console.log('Algorithm changed to:', this.value);
        });
    }
});

/**
 * Process image with selected algorithm
 */
async function processImage() {
    if (!window.uploadedFilename) {
        showMessage('Vui lòng upload ảnh trước', 'error');
        return;
    }

    // Get selected algorithm
    const algorithm = algorithmSelect.value;

    // Get enhancement options
    const enhanceCheckboxes = document.querySelectorAll('input[name="enhance"]:checked');
    const enhance = Array.from(enhanceCheckboxes).map(cb => cb.value);

    console.log('Processing with:', { algorithm, enhance });

    // Show loading, hide message
    showLoading();
    hideMessage();

    // Disable process button
    processBtn.disabled = true;

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: window.uploadedFilename,
                algorithm: algorithm,
                enhance: enhance
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            console.log('Processing successful:', data);

            // Show success message briefly
            showMessage(
                `Xử lý thành công! Thời gian: ${data.process_time}s`,
                'success'
            );

            // Redirect to result page after brief delay
            setTimeout(() => {
                window.location.href = `/result?original=${data.original_filename}&output=${data.output_filename}`;
            }, 1000);
        } else {
            throw new Error(data.error || 'Xử lý thất bại');
        }
    } catch (error) {
        console.error('Processing error:', error);
        showMessage('Lỗi khi xử lý: ' + error.message, 'error');
        hideLoading();
        processBtn.disabled = false;
    }
}

/**
 * Show loading spinner
 */
function showLoading() {
    if (loadingDiv) {
        loadingDiv.classList.remove('hidden');
    }
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    if (loadingDiv) {
        loadingDiv.classList.add('hidden');
    }
}

/**
 * Show message to user
 * @param {string} text - Message text
 * @param {string} type - Message type ('success' or 'error')
 */
function showMessage(text, type = 'success') {
    if (messageDiv) {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.classList.remove('hidden');

        // Auto hide after 5 seconds
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }
}

/**
 * Hide message
 */
function hideMessage() {
    if (messageDiv) {
        messageDiv.classList.add('hidden');
    }
}

/**
 * Enable process button (called from upload.js after successful upload)
 * @param {string} filename - Uploaded filename
 */
function enableProcessing(filename) {
    window.uploadedFilename = filename;

    if (processBtn) {
        processBtn.disabled = false;
    }

    // Show controls section
    const controlsSection = document.getElementById('controls-section');
    if (controlsSection) {
        controlsSection.classList.remove('hidden');
    }

    console.log('Processing enabled for:', filename);
}

/**
 * Disable process button
 */
function disableProcessing() {
    window.uploadedFilename = null;

    if (processBtn) {
        processBtn.disabled = true;
    }

    // Hide controls section
    const controlsSection = document.getElementById('controls-section');
    if (controlsSection) {
        controlsSection.classList.add('hidden');
    }
}

/**
 * Format file size to human readable
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Validate image file
 * @param {File} file - File to validate
 * @returns {Object} Validation result with isValid and error
 */
function validateImageFile(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];

    if (!file) {
        return { isValid: false, error: 'Không có file được chọn' };
    }

    if (!allowedTypes.includes(file.type)) {
        return {
            isValid: false,
            error: 'File không hợp lệ. Chỉ chấp nhận: PNG, JPG, JPEG'
        };
    }

    if (file.size > maxSize) {
        return {
            isValid: false,
            error: 'File quá lớn. Kích thước tối đa: 16MB'
        };
    }

    return { isValid: true };
}
