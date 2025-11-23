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

    // Make drop zone clickable
    dropZone.addEventListener('click', function(e) {
        if (e.target !== fileInput) {
            fileInput.click();
        }
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
        showMessage(validation.error, 'error');
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
    showLoading();
    hideMessage();

    // Disable process button while uploading
    if (typeof disableProcessing === 'function') {
        disableProcessing();
    }

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            console.log('Upload successful:', data);

            showMessage('Upload thành công!', 'success');

            // Enable processing with uploaded filename
            if (typeof enableProcessing === 'function') {
                enableProcessing(data.filename);
            }
        } else {
            throw new Error(data.error || 'Upload thất bại');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showMessage('Lỗi khi upload: ' + error.message, 'error');

        // Clear preview on error
        clearPreview();
    } finally {
        hideLoading();
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
