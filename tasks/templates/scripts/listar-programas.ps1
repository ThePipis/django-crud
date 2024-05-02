param(
    [string[]]$ComputerName,
    [string]$Username,
    [string]$Password,
    [string]$FilePath = "C:\UninstallView.exe",
    [string]$JsonOutputPath = "C:\temp\NuevaPrueba.json"
)
function Invoke-UninstallViewRemotely {
    param(
        [string[]]$ComputerName,
        [string]$Username,
        [string]$Password,
        [string]$FilePath,
        [string]$JsonOutputPath
    )
    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    $Credential = New-Object System.Management.Automation.PSCredential ($Username, $SecurePassword)
    $allResults = @()
    $ScriptBlock = {
        param($FilePath, $JsonOutputPath)
        if (-not (Test-Path "C:\temp")) { 
            New-Item -Path "C:\temp" -ItemType Directory | Out-Null
        }
        if (Test-Path $FilePath) {
            $process = Start-Process $FilePath -ArgumentList "/sjson $JsonOutputPath" -NoNewWindow -PassThru -RedirectStandardOutput "C:\temp\output.txt" -RedirectStandardError "C:\temp\error.txt"
            $null = $process.WaitForExit(10000) # Espera hasta 10 segundos
            if (!$process.HasExited) {
                $null = $process.Kill() 
            } else { 
                if (Test-Path $JsonOutputPath) {
                    $jsonContent = Get-Content $JsonOutputPath -Raw
                    $jsonData = ConvertFrom-Json $jsonContent
                    return $jsonData
                }
            }
        } 
    }
    foreach ($server in $ComputerName) {
        $jsonObject = Invoke-Command -ComputerName $server -ScriptBlock $ScriptBlock -ArgumentList $FilePath, $JsonOutputPath -Credential $Credential
        $allResults += $jsonObject
    }
    return $allResults | ConvertTo-Json -Depth 5
}
 Invoke-UninstallViewRemotely -ComputerName $ComputerName -Username $Username -Password $Password -FilePath $FilePath -JsonOutputPath $JsonOutputPath