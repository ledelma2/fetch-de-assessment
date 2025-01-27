. .\config-helper.ps1
$composeFilePath = "..\..\compose.yml"
$configFilePath = "..\config\config.json"
$envFilePath = "..\config\.env"
$timeoutKey = "ComposeUpTimeout"
$timeout = $null
if(Test-JsonConfig -FilePath $configFilePath -or $null -ne ($timeout = Get-JsonConfigValue -FilePath $configFilePath -Key $timeoutKey)) {
    Write-Host "Running docker compose up with custom timeout $timeout"
    docker compose -f $composeFilePath --env-file $envFilePath up -d -t $timeout
}else {
    Write-Host "Running docker compose up with default timeout..."
    docker compose -f $composeFilePath --env-file $envFilePath up -d
}