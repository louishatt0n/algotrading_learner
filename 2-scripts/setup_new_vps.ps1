# setup_new_vps.ps1
# One-command VPS bootstrap for setup_server.sh + requirements.txt
#
# Usage:
#   .\2-scripts\setup_new_vps.ps1 -ServerIp "YOUR_SERVER_IP"
#
# Optional:
#   .\2-scripts\setup_new_vps.ps1 -ServerIp "YOUR_SERVER_IP" -User "root" -RemoteDir "/root"

param(
    [Parameter(Mandatory = $true)]
    [string]$ServerIp,

    [string]$User = "root",
    [string]$RemoteDir = "/root"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$setupScript = Join-Path $PSScriptRoot "setup_server.sh"
$requirements = Join-Path $projectRoot "requirements.txt"
$target = "$User@$ServerIp`:$RemoteDir/"
$sshTarget = "$User@$ServerIp"

if (-not (Test-Path $setupScript)) {
    throw "Missing file: $setupScript"
}

if (-not (Test-Path $requirements)) {
    throw "Missing file: $requirements"
}

Write-Host "Uploading setup files to $sshTarget ..."
scp $setupScript $requirements $target

Write-Host "Running remote bootstrap ..."
ssh $sshTarget "sed -i 's/\r$//' $RemoteDir/setup_server.sh && chmod +x $RemoteDir/setup_server.sh && REQUIREMENTS_FILE=$RemoteDir/requirements.txt $RemoteDir/setup_server.sh"

Write-Host ""
Write-Host "Bootstrap complete."
Write-Host "Tip: Re-run this script anytime to refresh setup."
