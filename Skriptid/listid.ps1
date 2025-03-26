Clear-Host
$numbers = @() # Tühi list
$numbers += 20
$numbers += 5
$numbers += 1999
#Write-Host $numbers

# Loo nimede list
$names = "Marko", "Juss", "Aino", "Anne", "Jänes"
#Write-Host $names

# Väljasta teine element
#Write-Host $numbers[1]
# Väljasta esimene element
#Write-Host $names[0]

# Listi suurus
#Write-Host $names.Length
#Write-Host $numbers.Length

# foreach loop
foreach($name in $names){
    Write-Host $name
}
Write-Host "___________________________________"

# for loop
for($x = 0; $x -lt $names.Length ;$x++){
    Write-Host $names[$x]
}
Write-Host "___________________________________"

# Väljasta kõikide nimede pikkus.
[int]$namesLenght = 0
foreach($name in $names){
    $namesLenght += $name.Length
}
Write-Host "Nimede pikkus kokku = $($namesLenght)"
Write-Host "___________________________________"

# Väljasta kõik nimed konsooli, iga nimi eraldi real, iga nime ette lisa järjekorra number koos punktiga
for($x = 0; $x -lt $names.Length ;$x++){
    Write-Host "$($x +1). $($names[$x])"
}

Write-Host "___________________________________"


<#
Ülesanne:
Väljasta mitu täishäälikut on kokku listis olevates nimedes.
#>
$vowels = @('a', 'e', 'i', 'o', 'u', 'õ', 'ä', 'ö', 'ü')
$vowelCount = 0
foreach ($name in $names) {
    foreach ($letter in $name.ToCharArray()) {
        if($vowels -contains $letter){
            $vowelCount++
        }
    }
}

Write-Host "Täishäälikuid kokku nimede listis = $($vowelCount)"

Write-Host "___________________________________"

Get-Random -Minimum 1 -Maximum 10

Write-Host "___________________________________"
