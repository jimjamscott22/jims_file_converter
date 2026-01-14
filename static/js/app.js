// Global state
let selectedFile = null;
let conversionResult = null;

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const previewImage = document.getElementById('previewImage');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const formatSelection = document.getElementById('formatSelection');
const outputFormat = document.getElementById('outputFormat');
const optionsSection = document.getElementById('optionsSection');
const qualityRange = document.getElementById('qualityRange');
const qualityValue = document.getElementById('qualityValue');
const resizeWidth = document.getElementById('resizeWidth');
const resizeHeight = document.getElementById('resizeHeight');
const convertButtonContainer = document.getElementById('convertButtonContainer');
const convertBtn = document.getElementById('convertBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultContainer = document.getElementById('resultContainer');
const resultMessage = document.getElementById('resultMessage');
const downloadBtn = document.getElementById('downloadBtn');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);
outputFormat.addEventListener('change', handleFormatChange);
qualityRange.addEventListener('input', handleQualityChange);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Handling
function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        showError('Please select a valid image file (JPEG, PNG, WebP, or GIF)');
        return;
    }
    
    // Validate file size (from template, default 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
        showError(`File is too large. Maximum size is ${maxSize / (1024 * 1024)}MB`);
        return;
    }
    
    selectedFile = file;
    displayFilePreview(file);
}

function displayFilePreview(file) {
    // Hide drop zone, show preview
    dropZone.classList.add('hidden');
    filePreview.classList.remove('hidden');
    formatSelection.classList.remove('hidden');
    optionsSection.classList.remove('hidden');
    
    // Display file info
    fileName.textContent = file.name;
    fileSize.textContent = formatBytes(file.size);
    
    // Display image preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    // Reset format selection
    outputFormat.value = '';
    convertButtonContainer.classList.add('hidden');
    updateQualityAvailability();
}

function handleFormatChange() {
    if (outputFormat.value) {
        convertButtonContainer.classList.remove('hidden');
    } else {
        convertButtonContainer.classList.add('hidden');
    }
    updateQualityAvailability();
}

function handleQualityChange() {
    qualityValue.textContent = qualityRange.value;
}

function updateQualityAvailability() {
    const format = outputFormat.value;
    const supportsQuality = ['jpeg', 'jpg', 'webp'].includes(format);
    
    qualityRange.disabled = !supportsQuality;
    if (!supportsQuality) {
        qualityValue.textContent = 'N/A';
    } else {
        qualityValue.textContent = qualityRange.value;
    }
}

// Conversion
async function convertFile() {
    if (!selectedFile || !outputFormat.value) {
        showError('Please select a file and output format');
        return;
    }
    
    // Hide convert button and format selection, show progress
    convertButtonContainer.classList.add('hidden');
    formatSelection.classList.add('hidden');
    optionsSection.classList.add('hidden');
    progressContainer.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
    
    // Disable convert button
    convertBtn.disabled = true;
    
    // Animate progress bar
    animateProgress();
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('output_format', outputFormat.value);
        
        // Optional conversion options
        if (['jpeg', 'jpg', 'webp'].includes(outputFormat.value)) {
            formData.append('quality', qualityRange.value);
        }
        
        const width = parseInt(resizeWidth.value, 10);
        if (!Number.isNaN(width)) {
            formData.append('resize_width', width);
        }
        
        const height = parseInt(resizeHeight.value, 10);
        if (!Number.isNaN(height)) {
            formData.append('resize_height', height);
        }
        
        // Send conversion request
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Conversion failed');
        }
        
        // Success
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';
        
        conversionResult = data;
        
        setTimeout(() => {
            showResult(data);
        }, 500);
        
    } catch (error) {
        console.error('Conversion error:', error);
        showError(error.message || 'An error occurred during conversion');
    } finally {
        convertBtn.disabled = false;
    }
}

function animateProgress() {
    progressFill.style.width = '0%';
    progressText.textContent = 'Uploading file...';
    
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += Math.random() * 10;
            progressFill.style.width = `${Math.min(progress, 90)}%`;
            
            if (progress < 30) {
                progressText.textContent = 'Uploading file...';
            } else if (progress < 60) {
                progressText.textContent = 'Converting image...';
            } else {
                progressText.textContent = 'Finalizing...';
            }
        } else {
            clearInterval(interval);
        }
    }, 300);
}

function showResult(data) {
    progressContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    
    resultMessage.textContent = `Successfully converted from ${data.input_format.toUpperCase()} to ${data.output_format.toUpperCase()}`;
}

function downloadFile() {
    if (conversionResult && conversionResult.download_url) {
        // Create a temporary anchor and trigger download
        const a = document.createElement('a');
        a.href = conversionResult.download_url;
        a.download = conversionResult.output_filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

// Error Handling
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
    progressContainer.classList.add('hidden');
    convertButtonContainer.classList.add('hidden');
    formatSelection.classList.add('hidden');
    optionsSection.classList.add('hidden');
}

function clearError() {
    errorContainer.classList.add('hidden');
    if (selectedFile) {
        formatSelection.classList.remove('hidden');
        optionsSection.classList.remove('hidden');
        if (outputFormat.value) {
            convertButtonContainer.classList.remove('hidden');
        }
    } else {
        reset();
    }
}

// Reset
function reset() {
    selectedFile = null;
    conversionResult = null;
    fileInput.value = '';
    outputFormat.value = '';
    qualityRange.value = '85';
    qualityValue.textContent = '85';
    resizeWidth.value = '';
    resizeHeight.value = '';
    
    dropZone.classList.remove('hidden');
    filePreview.classList.add('hidden');
    formatSelection.classList.add('hidden');
    optionsSection.classList.add('hidden');
    convertButtonContainer.classList.add('hidden');
    progressContainer.classList.add('hidden');
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
}

function clearFile() {
    reset();
}

// Utilities
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Jim\'s File Converter initialized');
    
    // Check API health
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data);
            if (!data.api_configured) {
                console.warn('⚠️ CloudConvert API key not configured');
            }
        })
        .catch(error => {
            console.error('Failed to check API health:', error);
        });
});
