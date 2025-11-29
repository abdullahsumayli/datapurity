<#
Health check script for DataPurity (Windows PowerShell 5.1 compatible)
- Checks backend health endpoint
- Optionally tests OCR endpoint with an image

Usage examples:
  .\health-check.ps1 -BaseUrl "https://aidotoo.com"
  .\health-check.ps1 -BaseUrl "https://aidotoo.com" -ImagePath "C:\\path\\to\\card.jpg"

Tip: For correct Arabic output, switch console to UTF-8:
  chcp 65001
#>

param(
    [string]$BaseUrl = "https://aidotoo.com",
    [string]$ImagePath
)

function Test-HttpOk($Url) {
    try {
        $resp = Invoke-WebRequest -Uri $Url -Method GET -UseBasicParsing -TimeoutSec 20
        return $resp.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

Write-Host "[1/2] Checking backend health at $BaseUrl/health ..."
if (Test-HttpOk "$BaseUrl/health") {
    Write-Host "OK: Backend health endpoint returned 200"
}
else {
    Write-Host "WARN: Backend health check failed (non-200 or unreachable)"
}

if ([string]::IsNullOrWhiteSpace($ImagePath)) {
    Write-Host "[2/2] Skipping OCR test (no -ImagePath provided)."
    Write-Host "To test OCR: .\\health-check.ps1 -BaseUrl '$BaseUrl' -ImagePath 'C:\\path\\to\\card.jpg'"
    exit 0
}

if (-not (Test-Path -LiteralPath $ImagePath)) {
    Write-Host "ERROR: Image not found: $ImagePath"; exit 1
}

# Prefer curl.exe for multipart form-data on Windows PowerShell 5.1
$curl = (Get-Command curl.exe -ErrorAction SilentlyContinue)
if (-not $curl) {
    Write-Host "ERROR: curl.exe not found. Install curl or run on PowerShell 7+ to use Invoke-WebRequest -Form."
    exit 1
}

Write-Host "[2/2] Testing OCR upload to $BaseUrl/api/v1/ocr/card ..."
# Note: Arabic may appear garbled in PowerShell 5.1 console; use chcp 65001
$proc = Start-Process -FilePath $curl.Source -ArgumentList @(
    '-s', '-X', 'POST', "$BaseUrl/api/v1/ocr/card",
    '-H', 'Expect:', # avoid 100-continue issues
    '-F', "file=@$ImagePath"
) -NoNewWindow -PassThru -Wait -RedirectStandardOutput stdout.txt -RedirectStandardError stderr.txt

$stdout = Get-Content -Raw -Path .\stdout.txt
$stderr = Get-Content -Raw -Path .\stderr.txt
Remove-Item .\stdout.txt, .\stderr.txt -ErrorAction SilentlyContinue

if ($proc.ExitCode -eq 0) {
    Write-Host "OCR request completed. Response snippet:"; 
    $snippet = if ($stdout.Length -gt 1000) { $stdout.Substring(0, 1000) + ' ...' } else { $stdout }
    Write-Output $snippet
    exit 0
}
else {
    Write-Host "ERROR: OCR request failed. STDERR:"; Write-Output $stderr
    exit 1
}
