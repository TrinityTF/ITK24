Clear-Host

$src = Join-Path -Path $PSScriptRoot -ChildPath 'Persons.csv' # Alg fail
$dst = Join-Path -Path $PSScriptRoot -ChildPath 'Persons-v2.csv' # Uus fail
$domeen = "@singedhaircut.gg" # Domeen
$header = "Eesnimi;Perenimi;Sünniaeg;Kasutajanimi;E-Mail" # Uus faili päis
$lineNr = 0

# Kontrollime, kas uus fail on olemas, kui on, siis eemalda
if (Test-Path $dst) {
    Remove-Item -Path $dst
    #Write-Host "Eemaldatud vana fail!"
} 

Out-File -FilePath $dst -Append -InputObject $header # Lisame päise

# Loeme faili sisu massiivi
$contents = Get-Content $src -Encoding "UTF8"

# Käime masiivi contents rea kaupa läbi.
for ($x = 1; $x -lt $contents.Length; $x++) {
    $line = $contents[$x]
    $lineNr++
    $parts = $line.Split(";")

    $firstname = $parts[0]
    $lastname = $parts[1]

    # Eemaldame tühikud ja sidekriipsud eesnimedest ja perenimedest
    $firstname = $firstname -replace " ", "" # Eemaldame tühiku
    $firstname = $firstname -replace "-", "" # Eemaldame sidekriipsu

    $lastname = $lastname -replace " ", "" # Eemaldame tühiku
    $lastname = $lastname -replace "-", "" # Eemaldame sidekriipsu

    # Teeme kasutajanime (eesnimi.perenimi)
    $username = $firstname + "." + $lastname
    $username = Remove-Diacritics -src $username.ToLower() # Eemaldame rõhumärgid

    # Teeme e-posti aadressi
    $email = $username + $domeen

    # Lisame rea uude faili
    $newLine = $parts[0] + ";" + $parts[1] + ";" + $parts[2] + ";" + $username + ";" + $email

    # Lisame rea uude faili
    Out-File -FilePath $dst -Append -InputObject $newLine

}

# Rõhumärkide eemaldamise funktsioon
function Remove-Diacritics {
    param ([String]$src = [String]::Empty)
    $normalized = $src.Normalize( [Text.NormalizationForm]::FormD )
    $sb = new-object Text.StringBuilder
    $normalized.ToCharArray() | ForEach-Object { 
        if ( [Globalization.CharUnicodeInfo]::GetUnicodeCategory($_) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($_)
        }
    }
    $sb.ToString()
}

# 
