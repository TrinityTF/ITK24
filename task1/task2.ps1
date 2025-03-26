# Loeb CSV faili
$users = Import-Csv -Path "new_users_accounts.csv" -Delimiter ";"

# Funktsioon kasutajate lisamiseks
function Add-AllUsers {
    $results = @()
    
    foreach ($user in $users) {
        $result = [PSCustomObject]@{
            Kasutajanimi = $user.Kasutajanimi
            Põhjus       = ""
            Edukas       = $false
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

            $result.Edukas = $true
            $results += $result
        }
        catch {
            $result.Põhjus = $_.Exception.Message
            $results += $result
        }
    }

    # Näita ainult lisatud tulemusi
    Clear-Host
    Write-Host "`nLisamise tulemused:" -ForegroundColor Cyan
    $results | Format-Table -AutoSize -Property Kasutajanimi, Edukas, Põhjus

    # Show Users group members
    Write-Host "`nKasutajad Users grupis:" -ForegroundColor Cyan
    Get-LocalGroupMember -Group "Users" | 
        Where-Object { $_.ObjectClass -eq "User" } | 
        ForEach-Object { Get-LocalUser -Name $_.Name.Split('\')[-1] } | 
        Select-Object Name, Enabled, Description | 
        Format-Table -AutoSize
}

# Funktsioon kasutaja kustutamiseks
function Remove-SingleUser {
    Clear-Host
    # Get only users that are members of the Users group
    $userList = @(Get-LocalGroupMember -Group "Users" | 
        Where-Object { $_.ObjectClass -eq "User" } | 
        ForEach-Object { Get-LocalUser -Name $_.Name.Split('\')[-1] } | 
        Select-Object Name, Enabled, Description)
    
    if ($userList.Count -eq 0) {
        Write-Host "Süsteemis pole ühtegi kasutajat Users grupis!" -ForegroundColor Yellow
        return
    }

    Write-Host "Olemasolevad kasutajad Users grupis:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $userList.Count; $i++) {
        Write-Host "$($i+1). $($userList[$i].Name)"
    }
    
    $choice = Read-Host "`nSisesta kustutatava kasutaja number (1-$($userList.Count))"
    
    if (-not ($choice -match '^\d+$')) {
        Write-Host "Vigane sisend! Palun sisesta number." -ForegroundColor Red
        return
    }
    
    $index = [int]$choice - 1
    if ($index -lt 0 -or $index -ge $userList.Count) {
        Write-Host "Vigane number! Palun vali 1-$($userList.Count)." -ForegroundColor Red
        return
    }
    
    $deleteUser = $userList[$index].Name
    
    try {
        # Remove user account
        Remove-LocalUser -Name $deleteUser
        Write-Host "Kasutaja $deleteUser kustutatud!" -ForegroundColor Green

        # Remove user profile folder
        $userProfilePath = "C:\Users\$deleteUser"
        if (Test-Path $userProfilePath) {
            Remove-Item -Path $userProfilePath -Force -Recurse -ErrorAction Stop
            Write-Host "Kasutaja profiili kaust kustutatud: $userProfilePath" -ForegroundColor Green
        }
        
        # Show updated list of Users group members
        Write-Host "`nUuendatud kasutajate nimekiri:" -ForegroundColor Cyan
        Get-LocalGroupMember -Group "Users" | 
            Where-Object { $_.ObjectClass -eq "User" } | 
            ForEach-Object { Get-LocalUser -Name $_.Name.Split('\')[-1] } | 
            Select-Object Name, Enabled, Description | 
            Format-Table -AutoSize
    }
    catch {
        Write-Host "Viga toimingu teostamisel: $_" -ForegroundColor Red
    }
}

# Peamenüü
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