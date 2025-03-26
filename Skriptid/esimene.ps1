Clear-Host # Puhasta ekraan
Get-Date # Get päev
<#
Multiline comment
 o 0
(___)
#>
$username = Read-Host -Prompt "Sisesta kasutajanimi" # Get user name
if ($username -eq $env:USERNAME){
    Write-Host "Tere tulemast $($username)!"
}
else{
    Write-Host "$username ei ole õige nimi!"
}
[int]$year = Read-Host "Sisesta aasta"
#$year.GetType()
if ($year -eq (Get-Date).Year){
    Write-Host "$year on käesolev aasta!"
} else {
    Write-Host "$year ei ole käesolev aasta"
}
# Küsi kasutaja nimi meetrites, kui see on alla ühe meetri ütle "kääbus", muul juhul "Normaalne" mõõt
[decimal]$height = Read-Host "Sisesta enda pikkus # m.cm #"
if ($height -lt 1) {
    Write-Host "$username on kääbus"
} else {
    Write-Host "$username on normaalset mõõtu"
}
# Väljasta pikkuse ruut ilma ise endaga korrutamata

function Get-Square($height){
    $result = [Math]::Pow($height,2)
    return $result
}
$pikkusRuudus = Get-Square($height)
Write-Host "Pikkus ruudus on: $pikkusRuudus"