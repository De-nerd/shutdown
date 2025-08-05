$startupPath = [Environment]::GetFolderPath("Startup")
$exePath = Join-Path $startupPath "power.exe"

$pids = Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $exePath } | Select-Object -ExpandProperty ProcessId

if ($pids) {
    $arguments = ($pids | ForEach-Object { "/PID $_" }) -join " "
    Start-Process taskkill -ArgumentList "$arguments /F"
}