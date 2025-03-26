# Failide lugemine
$firstNames = Get-Content -Path "Eesnimed.txt"
$lastNames = Get-Content -Path "Perenimed.txt"
$descriptions = Get-Content -Path "kirjeldused.txt"

# Funktsioon kasutajanime loomiseks
function New-Username($firstName, $lastName) {
    $firstName = $firstName -replace '[ \-]', '' | Out-String
    $lastName = $lastName -replace '[ \-]', '' | Out-String
    $username = "$($firstName.Trim()).$($lastName.Trim())".ToLower()
    return $username
}

# Funktsioon parooli genereerimiseks
function New-Password {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    $passwordLength = Get-Random -Minimum 5 -Maximum 9
    return -join ((1..$passwordLength) | ForEach-Object { $chars[(Get-Random -Maximum $chars.Length)] })
}

# Loodavate kasutajate arv
$userCount = 5
$users = @()

# Kasutajate genereerimine
for ($i = 0; $i -lt $userCount; $i++) {
    $firstName = $firstNames | Get-Random
    $lastName = $lastNames | Get-Random
    $description = $descriptions | Get-Random
    $username = New-Username $firstName $lastName
    $password = New-Password

    # Eemaldame tühikud ja sidekriipsud eesnimedest ja perenimedest
    $firstname = $firstname -replace " ", "" # Eemaldame tühiku
    $firstname = $firstname -replace "-", "" # Eemaldame sidekriipsu

    $lastname = $lastname -replace " ", "" # Eemaldame tühiku
    $lastname = $lastname -replace "-", "" # Eemaldame sidekriipsu
    
    $users += [PSCustomObject]@{
        Eesnimi     = $firstName
        Perenimi    = $lastName
        Kasutajanimi = $username
        Parool      = $password
        Kirjeldus   = $description
    }
}

# CSV-faili salvestamine
$users | Export-Csv -Path "new_users_accounts.csv" -Delimiter ";" -NoTypeInformation -Encoding UTF8

# Kuvamine konsoolis
Write-Host "Loodud kasutajad:" -ForegroundColor Green
$users | Format-Table -AutoSize
