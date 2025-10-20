// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    const triggerTabList = document.querySelectorAll('[data-bs-toggle="tab"]');
    triggerTabList.forEach(triggerEl => {
        const tabTrigger = new bootstrap.Tab(triggerEl);
        triggerEl.addEventListener('click', event => {
            event.preventDefault();
            tabTrigger.show();
        });
    });
    
    // Load data when tabs are shown
    document.querySelector('a[href="#models"]')?.addEventListener('shown.bs.tab', loadModels);
    document.querySelector('a[href="#health"]')?.addEventListener('shown.bs.tab', loadHealth);
    
    // Set up form handlers
    setupUploadForm();
    setupIngestForm();
    
    // Load initial data
    loadModels();
});

// Upload form setup
function setupUploadForm() {
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('file', document.getElementById('modelFile').files[0]);
        formData.append('name', document.getElementById('modelName').value);
        formData.append('version', document.getElementById('modelVersion').value);
        
        try {
            const response = await fetch('/api/package', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showAlert('uploadResult', `Model uploaded successfully! ID: ${result.id}`, 'success');
                document.getElementById('uploadForm').reset();
            } else {
                showAlert('uploadResult', `Error: ${result.detail || 'Upload failed'}`, 'danger');
            }
        } catch (error) {
            showAlert('uploadResult', `Error: ${error.message}`, 'danger');
        }
    });
}

// Ingest form setup
function setupIngestForm() {
    document.getElementById('ingestForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('huggingface_url', document.getElementById('hfUrl').value);
        
        try {
            const response = await fetch('/api/package/ingest', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showAlert('ingestResult', `Model ingested successfully! ID: ${result.id}`, 'success');
                document.getElementById('ingestForm').reset();
            } else {
                showAlert('ingestResult', `Error: ${result.detail || 'Ingest failed'}`, 'danger');
            }
        } catch (error) {
            showAlert('ingestResult', `Error: ${error.message}`, 'danger');
        }
    });
}

// Load models list
async function loadModels() {
    try {
        const response = await fetch('/api/packages');
        const models = await response.json();
        
        const modelsList = document.getElementById('modelsList');
        
        if (models.length === 0) {
            modelsList.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i> No models available yet. Upload one to get started!
                    </div>
                </div>
            `;
            return;
        }
        
        modelsList.innerHTML = models.map(model => `
            <div class="col-md-4 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${model.Name}</h5>
                        <p class="card-text">
                            <strong>Version:</strong> ${model.Version}<br>
                            <strong>ID:</strong> ${model.ID}
                        </p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-primary btn-sm" onclick="rateModel('${model.ID}', '${model.Name}')">
                            <i class="bi bi-bar-chart"></i> Rate
                        </button>
                        <button class="btn btn-success btn-sm" onclick="downloadModel('${model.ID}')">
                            <i class="bi bi-download"></i> Download
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

// Rate a model
async function rateModel(id, name) {
    try {
        const response = await fetch(`/api/package/${id}/rate`);
        const rating = await response.json();
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <h5>Rating for ${name}</h5>
            <div class="row">
                ${Object.entries(rating).map(([key, value]) => `
                    <div class="col-md-6 mb-3">
                        <strong>${key}:</strong>
                        <div class="progress" style="height: 25px;">
                            <div class="progress-bar ${getProgressColor(value)}" 
                                 role="progressbar" 
                                 style="width: ${value * 100}%"
                                 aria-valuenow="${value * 100}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${value.toFixed(2)}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('ratingModal'));
        modal.show();
    } catch (error) {
        alert(`Error rating model: ${error.message}`);
    }
}

// Get progress bar color
function getProgressColor(value) {
    if (value >= 0.8) return 'bg-success';
    if (value >= 0.5) return 'bg-warning';
    return 'bg-danger';
}

// Download model
function downloadModel(id) {
    window.location.href = `/api/package/${id}/download`;
}

// Load health
async function loadHealth() {
    try {
        const response = await fetch('/api/health');
        const health = await response.json();
        
        const dashboard = document.getElementById('healthDashboard');
        dashboard.innerHTML = `
            <div class="col-md-3 mb-3">
                <div class="card text-center ${health.status === 'healthy' ? 'border-success' : 'border-danger'}">
                    <div class="card-body">
                        <h1>${health.status === 'healthy' ? '✓' : '✗'}</h1>
                        <p class="card-text">Status: ${health.status}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center border-primary">
                    <div class="card-body">
                        <h1>${Math.floor(health.uptime / 3600)}h</h1>
                        <p class="card-text">Uptime</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center border-info">
                    <div class="card-body">
                        <h1>${health.requests_last_hour}</h1>
                        <p class="card-text">Requests (last hour)</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center border-warning">
                    <div class="card-body">
                        <h1>${health.models_count}</h1>
                        <p class="card-text">Total Models</p>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading health:', error);
    }
}

// Show alert
function showAlert(elementId, message, type) {
    const alertDiv = document.getElementById(elementId);
    alertDiv.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    setTimeout(() => {
        alertDiv.innerHTML = '';
    }, 5000);
}
