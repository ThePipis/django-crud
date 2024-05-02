param(
    [string]$ComputerName,
    [string]$Username,
    [string]$Password,
    [string]$FilePath = "C:\UninstallView.exe",
    [string]$JsonOutputPath = "C:\temp\NuevaPrueba.json"
)

function Invoke-UninstallViewRemotely {
    param(
        [string]$ComputerName,
        [string]$Username,
        [string]$Password,
        [string]$FilePath,
        [string]$JsonOutputPath
    )

    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    $Credential = New-Object System.Management.Automation.PSCredential ($Username, $SecurePassword)

    $ScriptBlock = {
        param($FilePath, $JsonOutputPath)
        #Write-Host "Iniciando el script con los siguientes parámetros:"
        #Write-Host "ComputerName: $using:ComputerName"
        #Write-Host "Username: $using:Username"
        #Write-Host "FilePath: $FilePath"
        #Write-Host "JsonOutputPath: $JsonOutputPath"

        # Crear la carpeta C:\temp si no existe
        if (-not (Test-Path "C:\temp")) {
            #Write-Host "La carpeta C:\temp no existe. Creando..."
            New-Item -Path "C:\temp" -ItemType Directory
        }

        # Verificar permisos de escritura
        if ((Get-Acl "C:\temp").Access | Where-Object {
            $_.FileSystemRights -match "Write" -and ($_.IdentityReference -match $using:Username -or $_.IdentityReference -like "*Administrators*")
        }) {
            #Write-Host "El usuario tiene permisos de escritura en C:\temp"
        } else {
            #Write-Host "Advertencia: El usuario NO tiene permisos de escritura en C:\temp"
        }

        # Verificar existencia de archivo y ejecutar
        #Write-Host "Verificando si el archivo existe en la ruta: $FilePath"
        if (Test-Path $FilePath) {
            #Write-Host "El archivo existe. Intentando ejecutar..."
            try {
                $process = Start-Process $FilePath -ArgumentList "/sjson $JsonOutputPath" -NoNewWindow -PassThru -RedirectStandardOutput "C:\temp\output.txt" -RedirectStandardError "C:\temp\error.txt"
                $null = $process.WaitForExit(10000) # Espera hasta 10 segundos
                if (!$process.HasExited) {
                    $null = $process.Kill()
                    #Write-Host "Proceso terminado debido a un tiempo de espera excesivo."
                } else {
                    #Write-Host "Proceso completado. Verifique los archivos de salida y error" 
                    if (Test-Path $JsonOutputPath) {
                        $jsonContent = Get-Content $JsonOutputPath -Raw
                        $jsonData = $jsonContent | ConvertFrom-Json
                        return $jsonData | ConvertTo-Json -Depth 5 | Write-Output
                    } else {
                        #Write-Host "El archivo JSON no fue encontrado después de la ejecución."
                    }
                }
            } catch {
                #Write-Host "Hubo un error al ejecutar el archivo: $_"
            }
        } else {
            #Write-Host "El archivo no existe en la ubicación especificada."
        }
    }

     $jsonObject = Invoke-Command -ComputerName $ComputerName -ScriptBlock $ScriptBlock -ArgumentList $FilePath, $JsonOutputPath -Credential $Credential
     return $jsonObject
}
Invoke-UninstallViewRemotely -ComputerName $ComputerName -Username $Username -Password $Password -FilePath $FilePath -JsonOutputPath $JsonOutputPath
