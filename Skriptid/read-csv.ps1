<#
    Liida kokku kasutaja poolt küsitud veerus olevad numbrid.
#>
Clear-Host
$src = Join-Path -Path $PSScriptRoot -ChildPath 'Create-MyCSV-v.csv'
$total = 0

function Get-Numeric ($string) { 
    return $string -match "^[\d\.]+$"
}

# Mitu veergu on failis?
$totalRows = (Get-Content $src -First 1).Split(";").Length

# Küsi kasutajalt sobivat veergu
[int]$column = Read-Host "Mitmes veerg kokku liita? [1 kuni $($totalRows)]"

# Kas kasutaja sisestas sobiva veeru?
if ($column -gt 0 -and $column -le $totalRows) {
    $column = $column - 1 # 0-based index
    $lines = [System.IO.File]::ReadLines($src)

    foreach ($line in $lines) {
        $parts = $line.Split(";")

        # Veendu, et veerg sisaldab väärtust, mida saab liita
        $value = $parts[$column].Trim()  
        
        # Kas veerg on numbriline?
        if (Get-Numeric($value)) {
            $total += [decimal]$value  
        }
    }
    Write-Host "Veeru summa on $total"
}
else {
    Write-Host "Veergu number on vale! [Lubatud 1- $totalRows]"
}
