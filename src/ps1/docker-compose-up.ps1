. .\config-helper.ps1
$configFilePath = "..\config\config.json"
$timeoutKey = "ComposeUpTimeout"
$timeout = $null
if(Test-JsonConfig -FilePath $configFilePath -or $null -ne ($timeout = Get-JsonConfigValue -FilePath $configFilePath -Key $timeoutKey)) {
    Write-Host "Running docker compose up with timeout $timeout"
    docker compose -f ..\..\compose.yml --env-file ..\config\.env up -d -t $timeout
}else {
    Write-Host "Running docker compose up with default timeout..."
    docker compose -f ..\..\compose.yml --env-file ..\config\.env up -d
}