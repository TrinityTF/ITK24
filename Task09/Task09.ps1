<#
.SYNOPSIS
    Skript Apache logifailide analüüsimiseks, toetab .gz faile.
#>

# --- Konfiguratsioon ---
$LogDirectory = "C:\Temp"
$LogFilePattern = "tuntud_access.*" # Leiab ka .gz failid
$OutputFile = "task09.txt"

$Global:BotNameExtractorRegex = '(?:\s|;|/\s*|[\(\[]|^)([a-zA-Z0-9\._-]*?(?:bot|crawler|robot)[a-zA-Z0-9\._-]*?)(?:/|[\s\);\]]|$)'

# --- Funktsioonid ---
function Extract-UserAgent {
    param ([string]$LogLine)
    if ($LogLine -match '"([^"]*)"$') { return $Matches[1] }
    return $null
}

function Get-DynamicBotName {
    param([string]$UserAgentString)
    if ([string]::IsNullOrWhiteSpace($UserAgentString)) { return $null }
    if ($UserAgentString -match $Global:BotNameExtractorRegex) {
        if ($Matches.Count -gt 1 -and -not [string]::IsNullOrWhiteSpace($Matches[1])) {
            $BotName = $Matches[1]
            $BotName = $BotName -replace "[/;,()\[\]\s].*$", ""
            $BotName = $BotName.Trim(" .,:;-")
            if (-not [string]::IsNullOrWhiteSpace($BotName)) { return $BotName }
        }
    }
    if ($UserAgentString -match 'bot') { return "GenericBot" }
    if ($UserAgentString -match 'crawler') { return "GenericCrawler" }
    if ($UserAgentString -match 'robot') { return "GenericRobot" }
    return $null
}

function Read-LogFileContent {
    param (
        [System.IO.FileInfo]$LogFile
    )
    if ($LogFile.Extension -eq ".gz") {
        try {
            $fileStream = $LogFile.OpenRead()
            $gzipStream = New-Object System.IO.Compression.GZipStream($fileStream, [System.IO.Compression.CompressionMode]::Decompress)
            $streamReader = New-Object System.IO.StreamReader($gzipStream, [System.Text.Encoding]::UTF8)
            
            $lines = New-Object System.Collections.Generic.List[string]
            while (($line = $streamReader.ReadLine()) -ne $null) {
                $lines.Add($line)
            }
            $streamReader.Close() # See sulgeb ka aluseks olevad striimid
            return $lines
        }
        catch [System.IO.InvalidDataException] { # Püüab kinni BadGzipFile erindi
            Write-Warning "  Viga: Fail $($LogFile.FullName) ei ole korrektne gzip fail või on vigane. Jätan vahele."
            return $null
        }
        catch {
            Write-Warning "  Viga .gz faili $($LogFile.FullName) lugemisel: $($_.Exception.Message)"
            return $null
        }
    } else {
        try {
            return Get-Content -Path $LogFile.FullName -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        catch {
            Write-Warning "  Viga faili $($LogFile.FullName) lugemisel: $($_.Exception.Message)"
            return $null
        }
    }
}

# --- Põhiloogika ---
# ... (algus sarnane eelmisele PS skriptile) ...
$LogFiles = Get-ChildItem -Path $LogDirectory -Filter $LogFilePattern -File -ErrorAction SilentlyContinue
if (-not $LogFiles) {
    # ... (veateade) ...
    exit 1
}

$BotCounts = @{} 
$UnidentifiedBotsExamples = [System.Collections.Generic.List[string]]::new()

foreach ($LogFileItem in $LogFiles) {
    Write-Host "Töötlen faili: $($LogFileItem.FullName)"
    $lines = Read-LogFileContent -LogFile $LogFileItem
    
    if ($null -eq $lines) {
        continue # Jäta see fail vahele, kui lugemine ebaõnnestus
    }

    foreach ($lineContent in $lines) {
        $UserAgent = Extract-UserAgent -LogLine $lineContent
        if ($UserAgent) {
            $BotName = Get-DynamicBotName -UserAgentString $UserAgent
            if ($BotName) {
                if ($BotCounts.ContainsKey($BotName)) { $BotCounts[$BotName]++ } 
                else { $BotCounts[$BotName] = 1 }
            } elseif (($UserAgent -match 'bot' -or $UserAgent -match 'crawler' -or $UserAgent -match 'robot') -and $UnidentifiedBotsExamples.Count -lt 10) {
                $UnidentifiedBotsExamples.Add($UserAgent)
            }
        }
    }
}
# ... (ülejäänud skript on sama, mis eelmine PS versioon väljundi osas) ...

if ($UnidentifiedBotsExamples.Count -gt 0) {
    Write-Host "`nMärkus: Mõned potentsiaalsed bot'id jäid identifitseerimata või üldistati. Näited UA stringidest:" -ForegroundColor Yellow
    foreach ($uaExample in $UnidentifiedBotsExamples) {
        Write-Host "  - $uaExample" -ForegroundColor Yellow
    }
    Write-Host "Võib vajada `$BotNameExtractorRegex täpsustamist.`n" -ForegroundColor Yellow
}


if ($BotCounts.Count -eq 0) {
    $NoBotsMessage = "Ühtegi bot'i (bot, crawler, robot) ei leitud kasutajaagentidest."
    Write-Host $NoBotsMessage
    Set-Content -Path $OutputFile -Value $NoBotsMessage -Encoding UTF8
    exit 0
}

$SortedBotsData = $BotCounts.GetEnumerator() | Sort-Object -Property @{Expression={$_.Value}; Descending=$true}, @{Expression={$_.Name}; Ascending=$true}

$OutputObjects = foreach ($BotEntry in $SortedBotsData) {
    [PSCustomObject]@{
        Bot = $BotEntry.Name
        Num = $BotEntry.Value
    }
}

$HeaderTitle = "Leitud bot'id ja nende külastuste arv (dünaamiliselt eraldatud nimed):"
Write-Host "`n$HeaderTitle"
$OutputObjects | Format-Table -AutoSize 

$FileContent = @($HeaderTitle)
$MaxBotNameLength = ($OutputObjects.Bot | Measure-Object -Maximum -Property Length).Maximum
$MaxBotNameLength = [Math]::Max($MaxBotNameLength, 3) 
$NumColumnWidth = 5 

$ColumnHeader = "{0,-$MaxBotNameLength} | {1,$NumColumnWidth}" -f "Bot", "Num"
$Separator = "-" * ($MaxBotNameLength + 3 + $NumColumnWidth)

$FileContent += $ColumnHeader
$FileContent += $Separator

foreach ($item in $OutputObjects) {
    $FileContent += "{0,-$MaxBotNameLength} | {1,$NumColumnWidth}" -f $item.Bot, $item.Num
}

try {
    Set-Content -Path $OutputFile -Value $FileContent -Encoding UTF8
    Write-Host "`nTulemused salvestatud faili $OutputFile"
}
catch {
    Write-Error "Viga faili $OutputFile kirjutamisel: $($_.Exception.Message)"
}

Write-Host "Skripti töö lõpetatud."