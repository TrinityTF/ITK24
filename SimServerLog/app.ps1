# -*- coding: utf-8 -*-
<#
.DESCRIPTION
  See skript teostab järgmised toimingud:
  1. Otsib c:\Temp kaustast kõiki faile, mille nimi algab "application.".
  2. Loeb leitud failide sisu rida-realt.
  3. Eraldab logiridadelt spetsiifilist infot kasutades regulaaravaldisi:
     - Üleslaetud failide nimed
     - Kasutajanimed (erinevatest kontekstidest)
     - Andmebaaside nimed (ühenduse loomisel/kaotamisel)
     - Arhiveerimise aadressid/failinimed (varundamine/taastamine)
     - Taaskäivitatud/uuendatud süsteemide nimed
     - Saadetud/vastu võetud teated
     - E-maili aadressid
     - Kuupäevad ja kellaajad
  4. Leiab kõige varasema ja hiliseima kuupäeva logides.
  5. Tuvastab ja loendab duplikaate igas kategoorias.
  6. Väljastab konsooli koondinfo (leitud kirjete arvud, min/max kuupäevad).
  7. Genereerib Exceli dokumendi detailse infoga (kõik leitud kirjed, duplikaadid).
#>

# --- Konfiguratsioon ---
$logDirectory = "c:\Temp"
$logFilePattern = "application.*"

# Loo failinimi koos ajaga, et vältida üle kirjutamist
$timestampFormat = "yyyyMMdd_HHmmss"
$currentTimestamp = Get-Date -Format $timestampFormat
# Salvesta Excel väljund samasse kausta, kus skript
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
$outputDocumentName = "LogiAnalüüs_$($currentTimestamp).xlsx"
$outputDocumentPath = Join-Path -Path $scriptDirectory -ChildPath $outputDocumentName

# Veendu, et sihtkaust eksisteerib faili salvestamiseks
if (-not (Test-Path -Path $scriptDirectory -PathType Container)) {
    Write-Warning "Väljundi kausta ($scriptDirectory) ei leitud. Luuakse kaust."
    try {
        New-Item -Path $scriptDirectory -ItemType Directory -ErrorAction Stop | Out-Null
    } catch {
        Write-Error "Ei suutnud luua kausta $scriptDirectory. Skripti töö peatatud."
        exit 1
    }
}

# --- Andmestruktuurid info kogumiseks ---
$allLines = @()
$uploadedFiles = [System.Collections.Generic.List[string]]::new()
$userNames = [System.Collections.Generic.List[string]]::new()
$databaseNames = [System.Collections.Generic.List[string]]::new()
$archivePaths = [System.Collections.Generic.List[string]]::new()
$systemEvents = [System.Collections.Generic.List[string]]::new()
$notifications = [System.Collections.Generic.List[string]]::new()
$emailAddresses = [System.Collections.Generic.List[string]]::new()
$timestamps = [System.Collections.Generic.List[datetime]]::new()

# --- Regulaaravaldised info eraldamiseks ---
$regexTimestamp = '\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]'
$regexUploadedFile = 'File uploaded - (.*)'
$regexUserName = '(?:User logged in|Error: Invalid password|User password changed|New user registered|Admin privileges granted|User profile updated|User logged out) - (?!N/A)(.*)'
$regexDatabaseName = 'Database connection (?:lost|established) - (.*)'
$regexArchivePath = 'Backup (?:created|restored) - (.*)'
$regexSystemEvent = 'System (?:update initiated|rebooted) - (.*)'
$regexNotification = 'Notification (?:sent|received) - (.*)'
$regexEmailAddress = 'Email (?:sent|received) - ([\w\.\-]+@[\w\.\-]+\.\w+)'

# --- Logifailide töötlemine ---
Write-Host "Alustan logifailide töötlemist kaustas $logDirectory..."

$logFiles = Get-ChildItem -Path $logDirectory -Filter $logFilePattern -File -ErrorAction SilentlyContinue

if ($logFiles.Count -eq 0) {
    Write-Error "Ei leidnud ühtegi '$logFilePattern' faili kaustast '$logDirectory'. Skripti töö peatatud."
    exit 1
}

foreach ($logFile in $logFiles) {
    Write-Host "Töötlen faili: $($logFile.FullName)"
    try {
        if ($logFile.Extension -eq ".gz") {
            # Loe GZip-faili sisu
            $fs = [System.IO.File]::OpenRead($logFile.FullName)
            $gz = New-Object System.IO.Compression.GzipStream($fs, [System.IO.Compression.CompressionMode]::Decompress)
            $sr = New-Object System.IO.StreamReader($gz, [System.Text.Encoding]::UTF8)
            $lines = @()
            while (-not $sr.EndOfStream) {
                $lines += $sr.ReadLine()
            }
            $sr.Close()
            $gz.Close()
            $fs.Close()
        } else {
            # Loe tavalist faili
            $lines = Get-Content -Path $logFile.FullName -Encoding UTF8 -ErrorAction Stop
        }
    } catch {
         Write-Warning "Viga faili '$($logFile.FullName)' lugemisel: $($_.Exception.Message). Jätkan järgmise failiga."
         continue # Jäta see fail vahele ja jätka järgmisega
    }


    foreach ($line in $lines) {
        $allLines += $line

        if ($line -match $regexTimestamp) {
            try {
                $currentTimestamp = [datetime]::ParseExact($Matches[1], 'yyyy-MM-dd HH:mm:ss', $null)
                $timestamps.Add($currentTimestamp)
            } catch {
                Write-Warning "Ei suutnud tuvastada kuupäeva real: $line"
            }
        }

        if ($line -match $regexUploadedFile) { $uploadedFiles.Add($Matches[1].Trim()) }
        if ($line -match $regexUserName) { $userNames.Add($Matches[1].Trim()) }
        if ($line -match $regexDatabaseName) { $databaseNames.Add($Matches[1].Trim()) }
        if ($line -match $regexArchivePath) { $archivePaths.Add($Matches[1].Trim()) }
        if ($line -match $regexSystemEvent) { $systemEvents.Add($Matches[1].Trim()) }
        if ($line -match $regexNotification) { $notifications.Add($Matches[1].Trim()) }
        if ($line -match $regexEmailAddress) { $emailAddresses.Add($Matches[1].Trim()) }
    }
}

Write-Host "Logifailide lugemine lõpetatud."

# --- Andmete analüüs ---
$minDate = $null
$maxDate = $null
if ($timestamps.Count -gt 0) {
    $sortedTimestamps = $timestamps | Sort-Object
    $minDate = $sortedTimestamps[0]
    $maxDate = $sortedTimestamps[-1]
}

# --- Duplikaatide leidmise funktsioon ---
function Get-Duplicates {
    param(
        [System.Collections.Generic.List[string]]$ItemList
    )
    # Veendu, et sisend pole tühi, et vältida vigu Group-Object'is
    if ($null -eq $ItemList -or $ItemList.Count -eq 0) {
        return @()
    }
    $duplicates = $ItemList | Group-Object | Where-Object { $_.Count -gt 1 } | Sort-Object Name
    return $duplicates
}
# --- Duplikaatide leidmine ---
$duplicateFiles = Get-Duplicates $uploadedFiles
$duplicateUsers = Get-Duplicates $userNames
$duplicateDatabases = Get-Duplicates $databaseNames
$duplicateArchives = Get-Duplicates $archivePaths
$duplicateSystems = Get-Duplicates $systemEvents
$duplicateNotifications = Get-Duplicates $notifications
$duplicateEmails = Get-Duplicates $emailAddresses

# --- Konsooli väljund ---
Write-Host "`n========== KOONDINFO ==========`n"
Write-Host "Analüüsitud failid:"
Write-Host "-----------------------"
Write-Host ($logFiles.Name -join "`n")

Write-Host "`nLeitud kirjed:"
Write-Host "-----------------------"
Write-Host "1. Üleslaetud failid: $($uploadedFiles.Count)"
Write-Host "2. Kasutajanimed: $($userNames.Count)"
Write-Host "3. Andmebaaside nimed: $($databaseNames.Count)"
Write-Host "4. Arhiveerimise aadressid: $($archivePaths.Count)"
Write-Host "5. Süsteemide taaskäivitused/uuendused: $($systemEvents.Count)"
Write-Host "6. Teated (saadetud/vastu võetud): $($notifications.Count)"
Write-Host "7. E-maili aadressid: $($emailAddresses.Count)"

Write-Host "`nLogiperiood:"
Write-Host "-----------------------"
if ($minDate -ne $null -and $maxDate -ne $null) {
    Write-Host "Vanim: $($minDate.ToString($outputDateFormat))"
    Write-Host "Uusim: $($maxDate.ToString($outputDateFormat))"
} else {
    Write-Host "Kuupäevasid ei leitud"
}

$totalDuplicates = @($duplicateFiles, $duplicateUsers, $duplicateDatabases, 
                     $duplicateArchives, $duplicateSystems, $duplicateNotifications, 
                     $duplicateEmails) | Where-Object { $_.Count -gt 0 } | Measure-Object | Select-Object -ExpandProperty Count

Write-Host "`nDuplikaadid:"
Write-Host "-----------------------"
if ($totalDuplicates -gt 0) {
    Write-Host "Leiti kokku $totalDuplicates kategoorias"
    if ($duplicateFiles.Count -gt 0) { Write-Host "- Üleslaetud failides" }
    if ($duplicateUsers.Count -gt 0) { Write-Host "- Kasutajanimedes" }
    if ($duplicateDatabases.Count -gt 0) { Write-Host "- Andmebaasi nimedes" }
    if ($duplicateArchives.Count -gt 0) { Write-Host "- Arhiveerimise aadressides" }
    if ($duplicateSystems.Count -gt 0) { Write-Host "- Süsteemi sündmustes" }
    if ($duplicateNotifications.Count -gt 0) { Write-Host "- Teadetes" }
    if ($duplicateEmails.Count -gt 0) { Write-Host "- E-mail aadressides" }
} else {
    Write-Host "Duplikaate ei leitud"
}

Write-Host "`nDetailne info:"
Write-Host "-----------------------"
Write-Host "Salvestatud: $outputDocumentPath"
Write-Host "`n==============================`n"

# --- Excel faili genereerimine ---
Write-Host "Alustan Excel faili genereerimist: $outputDocumentPath"

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $workbook = $excel.Workbooks.Add()

    # Lisa analüüsitud failide leht
    $sheet = $workbook.Sheets.Item(1)
    $sheet.Name = "Failid"
    $sheet.Cells.Item(1,1) = "Analüüsitud failid"
    $i = 2
    foreach ($fname in $logFiles.Name) {
        $sheet.Cells.Item($i,1) = $fname
        $i++
    }

    # Lisa kategooriad eraldi lehtedena
    $categories = @(
        @{ Title = "Üleslaetud failid"; Items = $uploadedFiles; Duplicates = $duplicateFiles },
        @{ Title = "Kasutajanimed"; Items = $userNames; Duplicates = $duplicateUsers },
        @{ Title = "Andmebaaside nimed"; Items = $databaseNames; Duplicates = $duplicateDatabases },
        @{ Title = "Arhiveerimise aadressid"; Items = $archivePaths; Duplicates = $duplicateArchives },
        @{ Title = "Süsteemide sündmused"; Items = $systemEvents; Duplicates = $duplicateSystems },
        @{ Title = "Teated"; Items = $notifications; Duplicates = $duplicateNotifications },
        @{ Title = "E-maili aadressid"; Items = $emailAddresses; Duplicates = $duplicateEmails }
    )

    foreach ($category in $categories) {
        $sheet = $workbook.Sheets.Add()
        $sheet.Name = $category.Title.Substring(0, [Math]::Min(28, $category.Title.Length)) # Excel piirang
        $sheet.Cells.Item(1,1) = $category.Title
        $sheet.Cells.Item(2,1) = "Kirje"
        $i = 3
        foreach ($item in $category.Items) {
            $sheet.Cells.Item($i,1) = $item
            $i++
        }
        # Duplikaadid
        $sheet.Cells.Item(1,3) = "Duplikaadid"
        $sheet.Cells.Item(2,3) = "Kirje"
        $sheet.Cells.Item(2,4) = "Kordi"
        $j = 3
        foreach ($dup in $category.Duplicates) {
            $sheet.Cells.Item($j,3) = $dup.Name
            $sheet.Cells.Item($j,4) = $dup.Count
            $j++
        }
    }

    # Lisa logiperioodi leht
    $sheet = $workbook.Sheets.Add()
    $sheet.Name = "Logiperiood"
    $sheet.Cells.Item(1,1) = "Logiperiood"
    if ($minDate -ne $null -and $maxDate -ne $null) {
        $sheet.Cells.Item(2,1) = "Vanim logikirje"
        $sheet.Cells.Item(2,2) = $minDate.ToString("yyyy-MM-dd HH:mm:ss")
        $sheet.Cells.Item(3,1) = "Uusim logikirje"
        $sheet.Cells.Item(3,2) = $maxDate.ToString("yyyy-MM-dd HH:mm:ss")
    } else {
        $sheet.Cells.Item(2,1) = "Kuupäevasid ei leitud."
    }

    # Salvesta ja sulge
    $workbook.SaveAs($outputDocumentPath, 51) # 51 = xlOpenXMLWorkbook (.xlsx)
    $workbook.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

    Write-Host "Excel fail '$outputDocumentPath' on edukalt loodud."
} catch {
    Write-Error "Excel faili salvestamisel tekkis viga: $($_.Exception.Message)"
    if ($excel) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}

Write-Host "Skripti töö lõpetatud."