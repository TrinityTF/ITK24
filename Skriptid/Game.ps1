<#
    This script is a simple game that asks the user to guess a number between 1 and 100, + Back door.
#>
Clear-Host
$pc_nr = Get-Random -Minimum 1 -Maximum 100
$gameOver = $false
$Global:steps = 0 # Global variable
Read-Host "Mängu alustamiseks vajuta ENTER"

function LetsPlay {
    [int]$user_nr = Read-Host "Sisesta number"
    $Global:steps++
    
    if ($user_nr -eq 1000) {
        Write-Host "Mäng lõpetatud tagaukse kaudu!"
        return $true
    }
    elseif ($user_nr -gt $pc_nr) {
        Write-Host "Arv on väiksem"
    }
    elseif ($user_nr -lt $pc_nr) {
        Write-Host "Arv on suurem"
    }
    elseif ($user_nr -eq $pc_nr) {
        Write-Host "Õige number!"
        Write-Host "Arvasid ära $Global:steps sammuga"
        return $true
    }

    return $false
}

Write-Host "Arva ära number 1 ja 100 vahel"
while (-not $gameOver) {
    $gameOver = LetsPlay

    if ($gameOver) {
        $answer = Read-Host "Kas soovid uuesti mängida? [jah/ei]"
        if ($answer -eq "jah" -or $answer -eq "J" -or $answer -eq "j" -or $answer -eq "JAH") {
            $pc_nr = Get-Random -Minimum 1 -Maximum 100
            [System.Boolean]$gameOver = $false
            $Global:steps = 0
        }
        else {
            $gameOver = $true
        }
    }
}
Write-Host "Mäng on lõppenud!"
