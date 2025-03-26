# Funksioon mis teeb etteantud pikkusega suvalise stringi
function Get-RandomString {
    param (
        [Parameter(Mandatory=$true)]
        [int]$Length
    )

    if ($Length -lt 1 -or $Length -gt 1000) {
        $Length = 10
    }
    
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.ToCharArray()
    $result = ''

    for($x = 0; $x -lt $Length; $x++){
        $nr = Get-Random -Minimum 0 -Maximum $chars.Length
        $result += $chars[$nr]
    }
    
    return $result
}
Write-Host "___________________________________"
Write-Host "Suvaline string: $(Get-RandomString -Length 10)"
Write-Host "___________________________________"

function Get-FolderSize {
    param (
        [string]$FolderPath = "C:\Users\$env:USERNAME\Desktop"

    )
    if (Test-Path $FolderPath){
        $folder = Get-ChildItem -Recurse -Force $FolderPath
        $FolderSize = ($folder | Measure-Object -Property Length -Sum).Sum
        return $FolderSize
    } else {
        return $null
    }
}

Write-Host "Folderi suurus: $(Get-FolderSize -FolderPath "C:\Users\$env:USERNAME\Documents/skriptid")"
Write-Host "___________________________________"