# Loeb CSV faili
$users = Import-Csv -Path "new_users_accounts.csv" -Delimiter ";"

# Funktsioon kasutajate lisamiseks
function Add-AllUsers {
    $results = @()
    
    foreach ($user in $users) {
        $result = [PSCustomObject]@{
            Kasutajanimi = $user.Kasutajanimi
            Põhjus        = ""
            Edukas        = $false
        }

        # Kontrolli kasutaja olemasolu
        if (Get-LocalUser -Name $user.Kasutajanimi -ErrorAction SilentlyContinue) {
            $result.Põhjus = "Kasutaja on juba olemas"
            $results += $result
            continue
        }

        # Kontrolli kasutajanime pikkust
        if ($user.Kasutajanimi.Length -gt 20) {
            $result.Põhjus = "Kasutajanimi liiga pikk (max 20 tähemärki)"
            $results += $result
            continue
        }

        # Proovi kasutajat luua
        try {
            $password = ConvertTo-SecureString $user.Parool -AsPlainText -Force
            
            # Truncate description if needed
            $description = if ($user.Kirjeldus.Length -gt 48) {
                $user.Kirjeldus.Substring(0,45) + "..."
            } else {
                $user.Kirjeldus
            }

            $newUserParams = @{
                Name        = $user.Kasutajanimi
                FullName    = "$($user.Eesnimi) $($user.Perenimi)"
                Password    = $password
                Description = $description
            }
            
            $null = New-LocalUser @newUserParams
            Add-LocalGroupMember -Group "Users" -Member $user.Kasutajanimi
            
            # Määra parooli aegumine
            $adsiUser = [ADSI]"WinNT://$env:COMPUTERNAME/$($user.Kasutajanimi)"
            $adsiUser.PasswordExpired = 1
            $adsiUser.SetInfo()

            $result.Edekas = $true
            $results += $result
        }
        catch {
            
        }
    }

    # Näita tulemusi
    Clear-Host
    Write-Host "`nLisamise tulemused:" -ForegroundColor Cyan
    $results | Format-Table -AutoSize
    
    Write-Host "`nSüsteemis olevad kasutajad:" -ForegroundColor Cyan
    Get-LocalUser | Select-Object Name, Enabled, Description | Format-Table -AutoSize
}

# Funktsioon kasutaja kustutamiseks (sama jääb)
function Remove-SingleUser {
    Clear-Host
    $existingUsers = Get-LocalUser | Select-Object -ExpandProperty Name
    
    Write-Host "Olemasolevad kasutajad:" -ForegroundColor Cyan
    $existingUsers | ForEach-Object { Write-Host "- $_" }
    
    $deleteUser = Read-Host "`nSisesta kustutatava kasutaja nimi"
    
    if ($existingUsers -contains $deleteUser) {
        Remove-LocalUser -Name $deleteUser
        Write-Host "Kasutaja $deleteUser kustutatud!" -ForegroundColor Green
    }
    else {
        Write-Host "Kasutajat $deleteUser ei leitud!" -ForegroundColor Red
    }
    
    Write-Host "`nUuendatud kasutajate nimekiri:" -ForegroundColor Cyan
    Get-LocalUser | Select-Object Name, Enabled, Description | Format-Table -AutoSize
}

# Peamenüü (sama jääb)
function Show-Menu {
    Clear-Host
    Write-Host "`nVali tegevus:`n" -ForegroundColor Cyan
    Write-Host "1. Lisa kõik kasutajad süsteemi"
    Write-Host "2. Kustuta kasutaja"
    Write-Host "3. Välju`n"
}

do {
    Show-Menu
    $choice = Read-Host "Sisesta valik (1-3)"
    
    switch ($choice) {
        '1' {
            Add-AllUsers
            exit
        }
        '2' {
            Remove-SingleUser
            exit
        }
        '3' { exit }
        default {
            Write-Host "Vale valik! Proovi uuesti." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}
while ($true)