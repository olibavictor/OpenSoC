# Definir URLs e caminhos locais
$sysmonUrl = "https://download.sysinternals.com/files/Sysmon.zip"
$configUrl = "https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/refs/heads/master/sysmonconfig-export.xml"
$downloadPath = "$env:TEMP\Sysmon.zip"
$extractPath = "$env:TEMP\Sysmon"
$configPath = "$extractPath\sysmonconfig.xml"

# Criar diretório temporário
if (!(Test-Path $extractPath)) {
    New-Item -ItemType Directory -Path $extractPath | Out-Null
}

# Baixar o Sysmon
Write-Output "Baixando Sysmon..."
Invoke-WebRequest -Uri $sysmonUrl -OutFile $downloadPath

# Extrair Sysmon.zip
Write-Output "Extraindo Sysmon..."
Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force

# Baixar o arquivo de configuração do Sysmon
Write-Output "Baixando configuração do Sysmon..."
Invoke-WebRequest -Uri $configUrl -OutFile $configPath

# Verificar se o Sysmon.exe existe
$sysmonExe = Get-ChildItem -Path $extractPath -Filter "Sysmon64.exe" -Recurse | Select-Object -ExpandProperty FullName
if (-not $sysmonExe) {
    Write-Error "Sysmon64.exe não encontrado! Verifique o download e a extração."
    exit 1
}

# Instalar o Sysmon com a configuração baixada
Write-Output "Instalando Sysmon..."
Start-Process -FilePath $sysmonExe -ArgumentList "-accepteula -i $configPath" -Wait -NoNewWindow

Write-Output "Instalação do Sysmon concluída!"
