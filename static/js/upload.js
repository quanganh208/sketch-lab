/**
 * SketchLab - Upload Handler
 * Handles file upload, drag & drop, and preview
 */

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewSection = document.getElementById('preview-section');
const previewImage = document.getElementById('preview-image');
const fileNameEl = document.getElementById('file-name');
const fileSizeEl = document.getElementById('file-size');

/**
 * Initialize upload handlers
 */
document.addEventListener('DOMContentLoaded', function() {
    if (!dropZone || !fileInput) {
        console.warn('Upload elements not found');
        return;
    }

    // Setup drag and drop
    setupDragAndDrop();

    // Setup file input change
    fileInput.addEventListener('change', handleFileSelect);

    // Make drop zone clickable (except when clicking on button or input)
    dropZone.addEventListener('click', function(e) {
        // Prevent double-trigger if clicking on button or input
        if (e.target.tagName === 'BUTTON' || e.target === fileInput) {
            return;
        }
        // Don't trigger if clicking inside button
        if (e.target.closest('button')) {
            return;
        }
        fileInput.click();
    });
});

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
}

/**
 * Prevent default drag behaviors
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Highlight drop zone
 */
function highlight(e) {
    dropZone.classList.add('drag-over');
}

/**
 * Unhighlight drop zone
 */
function unhighlight(e) {
    dropZone.classList.remove('drag-over');
}

/**
 * Handle file drop
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        handleFile(files[0]);
    }
}

/**
 * Handle file select from input
 */
function handleFileSelect(e) {
    const files = e.target.files;

    if (files.length > 0) {
        handleFile(files[0]);
    }
}

/**
 * Handle file (validate, preview, upload)
 * @param {File} file - File to handle
 */
async function handleFile(file) {
    console.log('File selected:', file.name, file.size, file.type);

    // Validate file
    const validation = validateImageFile(file);

    if (!validation.isValid) {
        // Show error message
        const messageDiv = document.getElementById('message');
        if (messageDiv) {
            messageDiv.textContent = validation.error;
            messageDiv.className = 'message error';
            messageDiv.classList.remove('hidden');
            setTimeout(() => messageDiv.classList.add('hidden'), 5000);
        }
        return;
    }

    // Show preview
    showPreview(file);

    // Upload file
    await uploadFile(file);
}

/**
 * Show image preview
 * @param {File} file - Image file to preview
 */
function showPreview(file) {
    const reader = new FileReader();

    reader.onload = function(e) {
        if (previewImage) {
            previewImage.src = e.target.result;
        }

        if (fileNameEl) {
            fileNameEl.textContent = file.name;
        }

        if (fileSizeEl) {
            fileSizeEl.textContent = formatFileSize(file.size);
        }

        if (previewSection) {
            previewSection.classList.remove('hidden');
        }
    };

    reader.readAsDataURL(file);
}

/**
 * Upload file to server
 * @param {File} file - File to upload
 */
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    // Show loading
    const loadingDiv = document.getElementById('loading');
    const messageDiv = document.getElementById('message');
    const processBtn = document.getElementById('process-btn');
    const controlsSection = document.getElementById('controls-section');

    if (loadingDiv) loadingDiv.classList.remove('hidden');
    if (messageDiv) messageDiv.classList.add('hidden');

    // Disable process button while uploading
    if (processBtn) processBtn.disabled = true;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            console.log('Upload successful:', data);

            // Show success message
            if (messageDiv) {
                messageDiv.textContent = 'Upload thành công!';
                messageDiv.className = 'message success';
                messageDiv.classList.remove('hidden');
                setTimeout(() => messageDiv.classList.add('hidden'), 3000);
            }

            // Enable processing - store filename globally
            window.uploadedFilename = data.filename;

            // Enable process button
            if (processBtn) processBtn.disabled = false;

            // Show controls section
            if (controlsSection) controlsSection.classList.remove('hidden');
        } else {
            throw new Error(data.error || 'Upload thất bại');
        }
    } catch (error) {
        console.error('Upload error:', error);

        // Show error message
        if (messageDiv) {
            messageDiv.textContent = 'Lỗi khi upload: ' + error.message;
            messageDiv.className = 'message error';
            messageDiv.classList.remove('hidden');
        }

        // Clear preview on error
        clearPreview();
    } finally {
        // Hide loading
        if (loadingDiv) loadingDiv.classList.add('hidden');
    }
}

/**
 * Clear preview
 */
function clearPreview() {
    if (previewSection) {
        previewSection.classList.add('hidden');
    }

    if (previewImage) {
        previewImage.src = '';
    }

    if (fileNameEl) {
        fileNameEl.textContent = '';
    }

    if (fileSizeEl) {
        fileSizeEl.textContent = '';
    }

    if (fileInput) {
        fileInput.value = '';
    }
}

/**
 * Format bytes to human readable size
 * @param {number} bytes - Size in bytes
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
