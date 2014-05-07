strComputer = "."
 Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")        
Set colOperatingSystem = objWMIService.ExecQuery("Select * from Win32_OperatingSystem")

For Each objOperatingSystem in colOperatingSystem
ServicePack = objOperatingSystem.ServicePackMajorVersion
Version = objOperatingSystem.Version

Next

Wscript.Echo "This operating system is " + Version