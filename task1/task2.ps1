# Loeb CSV faili
$users = Import-Csv -Path "new_users_accounts.csv" -Delimiter ";"

# Funktsioon kasutaja lisamiseks
function Add-LocalUserAccount($user) {
    $existingUser = Get-LocalUser -Name $user.Kasutajanimi -ErrorAction SilentlyContinue
    if ($existingUser) {
        Write-Host "Kasutaja $($user.Kasutajanimi) on juba olemas!" -ForegroundColor Yellow
        return
    }
    
    if ($user.Kasutajanimi.Length -gt 20) {
        Write-Host "Kasutajanimi $($user.Kasutajanimi) on liiga pikk!" -ForegroundColor Red
        return
    }
    
    if ($user.Kirjeldus.Length -gt 48) {
        Write-Host "Kasutaja $($user.Kasutajanimi) kirjeldus on liiga pikk!" -ForegroundColor Red
        return
    }
    
    try {
        $password = ConvertTo-SecureString $user.Parool -AsPlainText -Force
        New-LocalUser -Name $user.Kasutajanimi -Password $password -Description $user.Kirjeldus -UserMayChangePassword $true -PasswordNeverExpires $false -FullName "$($user.Eesnimi) $($user.Perenimi)"
        Add-LocalGroupMember -Group "Users" -Member $user.Kasutajanimi
        # Määra parool aeguma
        Set-LocalUser -Name $user.Kasutajanimi -PasswordExpires $true
        # Sunni parooli muutmine järgmisel sisselogimisel
        Set-LocalUser -Name $user.Kasutajanimi -PasswordNeverExpires $false
        $account = [ADSI]"WinNT://$env:COMPUTERNAME/$($user.Kasutajanimi)"
        $account.PasswordExpired = 1
        $account.SetInfo()
        Write-Host "Kasutaja $($user.Kasutajanimi) lisatud süsteemi!" -ForegroundColor Green
    }
    catch {
        Write-Host "Viga kasutaja $($user.Kasutajanimi) lisamisel: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Funktsioon kasutaja kustutamiseks
function Remove-LocalUserAccount() {
    $existingUsers = Get-LocalUser | Select-Object -ExpandProperty Name
    Write-Host "Olemasolevad kasutajad:" -ForegroundColor Cyan
    $existingUsers | ForEach-Object { Write-Host $_ }
    
    $deleteUser = Read-Host "Sisesta kustutatava kasutaja nimi"
    
    if ($existingUsers -contains $deleteUser) {
        Remove-LocalUser -Name $deleteUser
        Write-Host "Kasutaja $deleteUser kustutatud!" -ForegroundColor Green
    } else {
        Write-Host "Kasutajat $deleteUser ei leitud!" -ForegroundColor Red
    }
}

# Peamenüü
Write-Host "Vali tegevus:" -ForegroundColor Cyan
Write-Host "1. Lisa kõik kasutajad süsteemi"
Write-Host "2. Kustuta kasutaja"

$choice = Read-Host "Sisesta valik (1 või 2)"

if ($choice -eq "1") {
    foreach ($user in $users) {
        Add-LocalUserAccount -user $user
    }
} elseif ($choice -eq "2") {
    Remove-LocalUserAccount
} else {
    Write-Host "Vale valik!" -ForegroundColor Red
}

# Kuvab kõik süsteemi kasutajad
Write-Host "Süsteemi kasutajad:" -ForegroundColor Cyan
Get-LocalUser | Select-Object Name, Description | Format-Table -AutoSize