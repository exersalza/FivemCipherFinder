$python_download_url = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
$python_path = ";C:\Program Files\Python312"

function Test-StringContains
{
    param(
        [string]$mainString,
        [string]$substring
    )

    if ($mainString -like "*$substring*")
    {
        return $true
    }
    else
    {
        return $false
    }
}

function Get-Python
{
    do
    {
        $answer = Read-Host -Prompt "Looks like you don't have python installed, you want to install? [y/n]"
    } until ($answer -eq "y" -or $answer -eq "n")

    if ($answer -ne "y")
    {
        Write-Error "Please install python manually or type 'y'"
        exit 1
    }

    Write-Output "Installing python ($python_download_url)"
    Invoke-WebRequest $python_download_url -OutFile ".\python312.exe"

    .\python312.exe /quiet InstallAllUsers = 1 PrependPath = 1
    Write-Output "Installed python. Setting the path variable"


    $old = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine')
    $new = $old + $python_path + $python_path + "\Scripts"
    [System.Environment]::SetEnvironmentVariable('PATH', $new, 'Machine')
}

$software = "Python";
$installed = (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
        Where { Test-StringContains -mainString $_.DisplayName -substring $software }) -ne $null

if (-Not$installed)
{
    Get-Python
}

do
{
    $answer = Read-Host -Prompt "Python is installed now. You want to continue installing the needed package? [y/n]"
} until ($answer -eq "y" -or $answer -eq "n")

if ($answer -eq "y")
{
    pip install fivemcipherfinder
    Write-Host
    Write-Host "Installed the finder, you can now run it with: find-cipher -p <YOUR SERVER RESOURCE PATH>"
}

Write-Host
Write-Host
Read-Host "Press <Enter> to exit..."
