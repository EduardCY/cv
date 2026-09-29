<#
PowerShell helper para crear e instalar el entorno virtual en `.venv`.
Ejecución (PowerShell):
    .\create_env.ps1

Esto crea `.venv`, actualiza pip e instala las dependencias desde requirements.txt.
#>

Write-Host "Creando/actualizando entorno virtual .venv..."

if (-Not (Test-Path -Path ".venv")) {
    python -m venv .venv
    Write-Host "Entorno virtual creado en .venv"
} else {
    Write-Host ".venv ya existe; se actualizará pip e instalarán dependencias"
}

Write-Host "Actualizando pip e instalando requirements.txt..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Hecho. Para activar el entorno (PowerShell):"
Write-Host "    .\\.venv\\Scripts\\Activate.ps1"
Write-Host "En VS Code la terminal se activará automáticamente si la configuración del workspace apunta a .venv."
