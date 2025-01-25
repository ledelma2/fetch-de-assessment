. .\config-helper.ps1
$configFilePath = "..\config\config.json"
$timeoutKey = "ComposeDownTimeout"
$timeout = $null
if(Test-JsonConfig -FilePath $configFilePath -or $null -ne ($timeout = Get-JsonConfigValue -FilePath $configFilePath -Key $timeoutKey)){
    Write-Host "Running docker compose down with timeout $timeout"
    docker compose -f ..\..\compose.yml --env-file ..\config\.env down -t $timeout
}else{
    Write-Host "Running docker compose down with default timeout..."
    docker compose -f ..\..\compose.yml --env-file ..\config\.env down
}