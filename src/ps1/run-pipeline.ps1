# Main loop control var
$script:running = $true

# Exit code
$ExitCode = 1

# Define a function to resolve the stop signal
function Resolve-StopSignal {
    Write-Host "Stop signal received. Gracefully shutting down..."
    Remove-Event -SourceIdentifier Console.CancelKeyPress
    $script:running = $false
}

# Main script for running the pipeline
try {
    # Register the handler
    Register-EngineEvent -SourceIdentifier Console.CancelKeyPress -Action {
        Resolve-StopSignal
    }
    # Set location to ps1 script directory
    Set-Location src\ps1
    # Run docker compose up script
    ./docker-compose-up.ps1
    # Log consumer data to a new terminal/shell window
    Start-Process powershell -ArgumentList '-NoExit', '-Command', 'docker compose logs -f my-python-consumer'
    Write-Host "Pipeline successfully started, waiting for user stop signal..."
    while ($script:running) {
        # Sleep until sigint or sigterm comes in from user
        Start-Sleep -Seconds 1
    }
    $ExitCode = 0
} catch {
    Write-Error "Unexpected error during pipeline ps1 script run..."
    $ExitCode = 1
} finally {
    # Run docker compose down script
    ./docker-compose-down.ps1
    Unregister-Event -SourceIdentifier Console.CancelKeyPress
    Set-Location ..\..
    Exit $ExitCode
}