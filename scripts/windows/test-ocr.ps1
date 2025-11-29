<#
Quick OCR test script (Windows PowerShell 5.1 compatible)

Usage:
  .\test-ocr.ps1 -BaseUrl "https://aidotoo.com" -ImagePath "C:\\path\\to\\card.jpg"

Tip: For correct Arabic output, switch console to UTF-8:
  chcp 65001
#>

param(
  [Parameter(Mandatory=$true)][string]$BaseUrl,
  [Parameter(Mandatory=$true)][string]$ImagePath
)

if (-not (Test-Path -LiteralPath $ImagePath)) {
  Write-Host "ERROR: Image not found: $ImagePath"; exit 1
}

$curl = (Get-Command curl.exe -ErrorAction SilentlyContinue)
if (-not $curl) {
  Write-Host "ERROR: curl.exe not found. Install curl or run on PowerShell 7+ to use Invoke-WebRequest -Form."
  exit 1
}

Write-Host "Posting to $BaseUrl/api/v1/ocr/card ..."
$proc = Start-Process -FilePath $curl.Source -ArgumentList @(
  '-s', '-X', 'POST', "$BaseUrl/api/v1/ocr/card",
  '-H', 'Expect:',
  '-F', "file=@$ImagePath"
) -NoNewWindow -PassThru -Wait -RedirectStandardOutput stdout.txt -RedirectStandardError stderr.txt

$stdout = Get-Content -Raw -Path .\stdout.txt
$stderr = Get-Content -Raw -Path .\stderr.txt
Remove-Item .\stdout.txt, .\stderr.txt -ErrorAction SilentlyContinue

if ($proc.ExitCode -eq 0) {
  Write-Output $stdout
  exit 0
} else {
  Write-Host "ERROR: OCR request failed. STDERR:"; Write-Output $stderr
  exit 1
}
