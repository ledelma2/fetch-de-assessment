. .\config-helper.ps1
$composeFilePath = "..\..\compose.yml"
$configFilePath = "..\config\config.json"
$envFilePath = "..\config\.env"
$timeoutKey = "ComposeDownTimeout"
$timeout = $null
if(Test-JsonConfig -FilePath $configFilePath -or $null -ne ($timeout = Get-JsonConfigValue -FilePath $configFilePath -Key $timeoutKey)){
    Write-Host "Running docker compose down with timeout $timeout"
    docker compose -f $composeFilePath --env-file $envFilePath down -t $timeout
}else{
    Write-Host "Running docker compose down with default timeout..."
    docker compose -f $composeFilePath --env-file $envFilePath down
}