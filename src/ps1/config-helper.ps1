function Test-JsonConfig {
    param (
        [string]$FilePath
    )
    if (-not (Test-Path $FilePath)) {
        Write-Error "Configuration file not found: $FilePath"
        return $false
    }

    try {
        Get-Content -Path $FilePath | ConvertFrom-Json
        return $true
    } catch {
        Write-Error "Failed to load or parse the configuration file: $FilePath"
        return $false
    }
    <#
        .SYNOPSIS
        Determines if a supplied config file is accesible and in json format.

        .DESCRIPTION
        This function reads a JSON file from the specified path and determines if the file is accesible and valid.

        .PARAMETER FilePath
        The path to the JSON configuration file.

        .OUTPUTS
        System.Boolean. Test-JsonConfig returns a boolean denoting if the supplied config file is accesible and valid.

        .EXAMPLE
        Test-Config -FilePath "./config.json"
        true

        .EXAMPLE
        Test-Config -FilePath "./config.png"
        false
    #>
}


function Get-JsonConfigValue {
    param (
        [string]$FilePath,
        [string]$Key
    )
    $Config = Get-Content -Path $FilePath | ConvertFrom-Json
    return $Config.$Key
    <#
        .SYNOPSIS
        Retrieves a specific key's value from a json config file or null if the key is missing.

        .DESCRIPTION
        This function attempts to return a value provided a valid key and filepath to a json config file.

        .PARAMETER FilePath
        The path to the JSON configuration file.

        .PARAMETER Key
        The key to retrieve from the configuration object.

        .OUTPUTS
        The value associated with the key, or null if the key is missing.

        .EXAMPLE
        Get-JsonConfigValue -FilePath "./config.json" -Key "Timeout"
        60

        .EXAMPLE
        Get-JsonConfigValue -FilePath "./config.json" -Key "MissingKey"
        null
    #>
}
