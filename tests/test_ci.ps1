# Search for the target directory upwards
function Search-ForDirectory {
    param (
        [string]$targetDir,
        [int]$maxAttempts
    )

    $currentDir = Get-Location
    $attempts = 0

    while ($attempts -lt $maxAttempts) {
        if (Test-Path "$currentDir\$targetDir") {
            Write-Host "Found $targetDir at $currentDir"
            Set-Location "$currentDir\$targetDir"
            return $true
        }

        # Move up one directory
        $currentDir = Split-Path $currentDir -Parent
        $attempts++
    }

    Write-Host "$targetDir not found after $maxAttempts attempts."
    return $false
}

# Search for the directory and change to it if found
Search-ForDirectory "light_distribution_analysis" 10

# Check if act is installed
if (!(Test-Path .\bin\act)) {
    Write-Host "act not found, downloading and installing..."
    # Download and install act
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/nektos/act/master/install.ps1" -OutFile "install.ps1"
    .\install.ps1
} else {
    Write-Host "act is already installed"
}

# Create .actrc file with default configuration
" -P ubuntu-latest=nektos/act-environments-ubuntu:18.04" | Out-File -FilePath .actrc

# Execute act
.\bin\act 2>&1 | Tee-Object -FilePath log.txt
