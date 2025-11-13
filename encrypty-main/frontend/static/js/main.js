// Tab switching functionality
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// File input handling
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', function(e) {
    fileList.innerHTML = '';
    const files = Array.from(e.target.files);
    
    if (files.length === 0) {
        fileList.innerHTML = '<p style="color: #888; text-align: center;">No files selected</p>';
        return;
    }
    
    files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.textContent = `${index + 1}. ${file.name} (${formatFileSize(file.size)})`;
        fileList.appendChild(fileItem);
    });
});

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Upload form handling
const uploadForm = document.getElementById('upload-form');
const uploadBtn = document.getElementById('upload-btn');

uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const files = fileInput.files;
    if (files.length === 0) {
        showError('Please select at least one file');
        return;
    }
    
    const action = document.querySelector('input[name="action"]:checked').value;
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    formData.append('action', action);
    
    setLoading(uploadBtn, true);
    hideResults();
    
    try {
        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(data.message, data.files || [], data.output);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        setLoading(uploadBtn, false);
    }
});

// Directory form handling
const directoryForm = document.getElementById('directory-form');
const directoryBtn = document.getElementById('directory-btn');

directoryForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const directory = document.getElementById('directory-input').value.trim();
    if (!directory) {
        showError('Please enter a directory path');
        return;
    }
    
    const action = document.querySelector('input[name="dir-action"]:checked').value;
    
    setLoading(directoryBtn, true);
    hideResults();
    
    try {
        const response = await fetch('/api/process-directory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                directory: directory,
                action: action
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(data.message, [], data.output, data.file_count);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        setLoading(directoryBtn, false);
    }
});

// UI helper functions
function setLoading(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const spinner = button.querySelector('.spinner');
    
    if (isLoading) {
        button.disabled = true;
        btnText.style.display = 'none';
        spinner.style.display = 'block';
    } else {
        button.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

function showSuccess(message, files, output, fileCount) {
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('results-content');
    const downloadSection = document.getElementById('download-section');
    const downloadLinks = document.getElementById('download-links');
    
    resultsContent.innerHTML = `
        <div class="success-message">
            <strong>✓ Success!</strong> ${message}
            ${fileCount ? `<br>Processed ${fileCount} file(s)` : ''}
        </div>
    `;
    
    if (output) {
        resultsContent.innerHTML += `
            <div class="output-text">${escapeHtml(output)}</div>
        `;
    }
    
    if (files && files.length > 0) {
        downloadLinks.innerHTML = '';
        files.forEach(file => {
            const link = document.createElement('a');
            link.href = `/api/download/${encodeURIComponent(file)}`;
            link.className = 'download-link';
            link.textContent = `Download ${file}`;
            link.download = file;
            downloadLinks.appendChild(link);
        });
        downloadSection.style.display = 'block';
    } else {
        downloadSection.style.display = 'none';
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('results-content');
    const downloadSection = document.getElementById('download-section');
    
    resultsContent.innerHTML = `
        <div class="error-message">
            <strong>✗ Error:</strong> ${escapeHtml(message)}
        </div>
    `;
    
    downloadSection.style.display = 'none';
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

