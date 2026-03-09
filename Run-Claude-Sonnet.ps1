$claudePath = "C:\Users\Honor\.local\bin\claude.exe"

if (-not (Test-Path $claudePath)) {
    Write-Error "Claude Code not found at $claudePath"
    exit 1
}

$projectRoot = "D:\Projects\Repos\MPNerveBot"
Set-Location $projectRoot

& $claudePath --model sonnet
