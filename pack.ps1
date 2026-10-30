$src = "C:\Users\ABID\Documents\Qoder\2026-10-29\908b8cf9"
$out = Join-Path ([Environment]::GetFolderPath('Desktop')) "InnoveCouture.zip"
if (Test-Path $out) { Remove-Item $out -Force }

# stage a clean copy so __pycache__ / logs stay out of the archive
$stage = Join-Path $env:TEMP "innove-pack"
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Path $stage | Out-Null
robocopy $src $stage /E /XD __pycache__ shots /XF server.log *.pyc /NFL /NDL /NJH /NJS /NP | Out-Null

Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $out -CompressionLevel Optimal
Remove-Item $stage -Recurse -Force

$z = Get-Item $out
"zip: $($z.FullName)"
"size: {0:N1} MB" -f ($z.Length / 1MB)
Add-Type -AssemblyName System.IO.Compression.FileSystem
$a = [System.IO.Compression.ZipFile]::OpenRead($out)
"entries: " + $a.Entries.Count
$a.Entries | Select-Object -First 12 | ForEach-Object { " - " + $_.FullName }
$a.Dispose()
