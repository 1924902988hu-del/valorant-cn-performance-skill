# VALORANT CN Performance Skill - read-only Windows diagnostic
# Version: 1.0.0 (2026-07-22)
# Prints JSON to stdout. It does not write files, change registry values, services,
# boot configuration, execution policy, drivers, Windows features, or anti-cheat.

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

function Read-Safely {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Action,
        [Parameter(Mandatory = $true)]$Fallback
    )
    try { return (& $Action) } catch { return $Fallback }
}

$os = Read-Safely { Get-CimInstance Win32_OperatingSystem } $null
$computer = Read-Safely { Get-CimInstance Win32_ComputerSystem } $null
$deviceGuard = Read-Safely {
    Get-CimInstance -Namespace 'root\Microsoft\Windows\DeviceGuard' -ClassName Win32_DeviceGuard
} $null

$cpu = @(Read-Safely {
    Get-CimInstance Win32_Processor | ForEach-Object {
        [ordered]@{
            name = $_.Name.Trim()
            physicalCores = $_.NumberOfCores
            logicalProcessors = $_.NumberOfLogicalProcessors
            currentClockMHz = $_.CurrentClockSpeed
            maxClockMHz = $_.MaxClockSpeed
        }
    }
} @())

$memoryModules = @(Read-Safely {
    Get-CimInstance Win32_PhysicalMemory | ForEach-Object {
        [ordered]@{
            capacityGB = [math]::Round($_.Capacity / 1GB, 1)
            configuredClockMTs = $_.ConfiguredClockSpeed
            ratedSpeedMTs = $_.Speed
            manufacturer = $_.Manufacturer
        }
    }
} @())

$gpus = @(Read-Safely {
    Get-CimInstance Win32_VideoController | ForEach-Object {
        [ordered]@{
            name = $_.Name
            driverVersion = $_.DriverVersion
            driverDate = $_.DriverDate
            currentResolution = if ($_.CurrentHorizontalResolution) {
                "{0}x{1}" -f $_.CurrentHorizontalResolution, $_.CurrentVerticalResolution
            } else { $null }
            currentRefreshHz = $_.CurrentRefreshRate
        }
    }
} @())

$powerPlan = Read-Safely { (powercfg /getactivescheme | Out-String).Trim() } 'unavailable'
$secureBoot = Read-Safely { [bool](Confirm-SecureBootUEFI) } 'unavailable-or-unsupported'
$tpm = Read-Safely {
    $value = Get-Tpm
    [ordered]@{
        present = [bool]$value.TpmPresent
        ready = [bool]$value.TpmReady
        enabled = [bool]$value.TpmEnabled
    }
} 'unavailable'

$vanguardServices = @(Read-Safely {
    Get-Service -Name 'vgc', 'vgk' -ErrorAction SilentlyContinue | ForEach-Object {
        [ordered]@{ name = $_.Name; status = [string]$_.Status }
    }
} @())

$aceProcesses = @(Read-Safely {
    Get-Process -Name 'SGuard*' -ErrorAction SilentlyContinue | ForEach-Object {
        [ordered]@{ name = $_.ProcessName }
    }
} @())

$chassisCodes = @(Read-Safely { (Get-CimInstance Win32_SystemEnclosure).ChassisTypes } @())
$laptopCodes = @(8, 9, 10, 14, 30, 31, 32)
$isLaptop = $false
foreach ($code in $chassisCodes) {
    if ($laptopCodes -contains [int]$code) { $isLaptop = $true }
}

$battery = @(Read-Safely {
    Get-CimInstance Win32_Battery | ForEach-Object {
        [ordered]@{
            estimatedChargePercent = $_.EstimatedChargeRemaining
            batteryStatus = $_.BatteryStatus
        }
    }
} @())

$disks = @(Read-Safely {
    Get-PhysicalDisk | ForEach-Object {
        [ordered]@{
            friendlyName = $_.FriendlyName
            mediaType = [string]$_.MediaType
            sizeGB = [math]::Round($_.Size / 1GB, 1)
        }
    }
} @())

$result = [ordered]@{
    schemaVersion = '1.0.0'
    collectedAt = (Get-Date).ToString('o')
    readOnly = $true
    privacy = [ordered]@{
        collectsPublicIp = $false
        collectsMacAddress = $false
        collectsAccountOrToken = $false
        note = 'Review the JSON before sharing; hardware and process/service names can still identify your setup.'
    }
    system = [ordered]@{
        caption = if ($os) { $os.Caption } else { 'unavailable' }
        version = if ($os) { $os.Version } else { 'unavailable' }
        buildNumber = if ($os) { $os.BuildNumber } else { 'unavailable' }
        lastBootTime = if ($os) { $os.LastBootUpTime } else { 'unavailable' }
        isLaptopHeuristic = $isLaptop
        chassisCodes = $chassisCodes
        hypervisorPresent = if ($computer) { [bool]$computer.HypervisorPresent } else { 'unavailable' }
    }
    cpu = $cpu
    memory = [ordered]@{
        totalGB = [math]::Round((($memoryModules | Measure-Object capacityGB -Sum).Sum), 1)
        modules = $memoryModules
        warning = 'WMI clock values do not prove XMP/EXPO or memory channel mode.'
    }
    gpuAndDisplays = $gpus
    powerPlan = $powerPlan
    battery = $battery
    security = [ordered]@{
        secureBoot = $secureBoot
        tpm = $tpm
        vbsStatus = if ($deviceGuard) { $deviceGuard.VirtualizationBasedSecurityStatus } else { 'unavailable' }
        securityServicesConfigured = if ($deviceGuard) { @($deviceGuard.SecurityServicesConfigured) } else { @() }
        securityServicesRunning = if ($deviceGuard) { @($deviceGuard.SecurityServicesRunning) } else { @() }
        note = 'These are observations, not instructions to disable Windows security.'
    }
    antiCheatHeuristics = [ordered]@{
        vanguardServices = $vanguardServices
        aceProcesses = $aceProcesses
        warning = 'Presence or absence is not definitive proof of server/account region.'
    }
    disks = $disks
    limitations = @(
        'Does not measure FPS, 1% lows, frame time, temperature, power limits, network RTT, or packet loss.',
        'Does not reliably detect IOMMU readiness or Vanguard On-Demand eligibility.',
        'Run the in-game baseline separately and provide the exact anti-cheat error text when relevant.'
    )
}

$result | ConvertTo-Json -Depth 8
