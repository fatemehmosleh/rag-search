# Activate venv (assumes .venv in repo root)
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    Write-Host "Activating virtualenv .venv"
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host ".venv not found. Activate your Python environment manually."
}

# Run the Flask app on port 8000 using the python -c runner
Write-Host "Starting Flask app on http://0.0.0.0:8000"
python -c "from app.app import app; app.run(host='0.0.0.0', port=8000)"
