<#
    Loe etteantud faili sisu ja tee igale isikule kasutajamini ja e-posti aadress.
    Kasutajanimi: eesnimi.perenimi, läbivalt väiksed tähed. Eesnimedes tühik ja sidekriips eemaldatud. Rõhumärgid asendataud.
    E-post: kasutajanimi@domeen
#>
Clear-Host

$src = Join-Path -Path $PSScriptRoot -ChildPath 'Persons.csv' # Alg fail
$dst = Join-Path -Path $PSScriptRoot -ChildPath 'Persons-v1.csv' # Uus fail
$domeen = "@singedhaircut.gg" # Domeen
$header = "Eesnimi;Perenimi;Sünniaeg;Kasutajanimi;E-Mail" # Uus faili päis

# Rõhumärkide eemaldamise funktsioon
function Remove-Diacritics {
    param ([String]$src = [String]::Empty)
    $normalized = $src.Normalize( [Text.NormalizationForm]::FormD )
    $sb = new-object Text.StringBuilder
    $normalized.ToCharArray() | ForeEach-Object { 
        if ( [Globalization.CharUnicodeInfo]::GetUnicodeCategory($_) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($_)
        }
    }
    $sb.ToString()
}

# Kontrollime, kas uus fail on olemas, kui on, siis eemalda
if (Test-Path $dst) {
    Remove-Item -Path $dst
    #Write-Host "Eemaldatud vana fail!"
} 

# Loeme faili sisu muutujasse  
$contents = Import-Csv -Path $src -Delimiter ";"
Out-File -FilePath $dst -Append -InputObject $header # Lisame päise

# Käime masiivi contents rea kaupa läbi.
foreach ($line in $contents){
    $firstname = $line.Eesnimi
    $lastname = $line.Perenimi

    # Eemaldame tühikud ja sidekriipsud eesnimedest ja perenimedest
    $firstname = $firstname -replace " ", "" # Eemaldame tühiku
    $firstname = $firstname -replace "-", "" # Eemaldame sidekriipsu

    $lastname = $lastname -replace " ", "" # Eemaldame tühiku
    $lastname = $lastname -replace "-", "" # Eemaldame sidekriipsu
    
    # Teeme kasutajanime (eesnimi.perenimi)
    $username = $firstname + "." + $lastname
    $username = Remove-Diacritics($username.ToLower()) # Eemaldame rõhumärgid
    

    # Teeme e-posti aadressi
    $email = $username + $domeen

    # Lisame rea uude faili
    # $newLine = "$($line.Eesnimi);$($line.Perenimi);$($line.Sünniaeg);$username;$email"
    $parts = @($line.Eesnimi, $line.Perenimi, $line.Sünniaeg, $username, $email)
    $newLine = $parts -join ";" # Liidame osad kokku

    # Lisame rea uude faili
    Out-File -FilePath $dst -Append -InputObject $newLine
}
