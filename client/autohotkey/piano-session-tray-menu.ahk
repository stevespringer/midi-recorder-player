varFolder := A_ScriptDir
FolderParent := SubStr(varFolder, 1, InStr(SubStr(varFolder,1,-1), "\", 0, 0)-1)
Ini := FolderParent . "\config.ini"

IniRead, TrayIconFile, %Ini%, Local, TrayIconFile
IniRead, DownloadFolder, %Ini%, Local, DownloadFolder
IniRead, MenuContentsFile, %Ini%, Local, MenuContentsFile
IniRead, Port, %Ini%, Remote, Port
IniRead, Host, %Ini%, Remote, Host

RunScript := "python.exe file-client.py --host " . Host . " --port " . Port

OnMessage(0x404,"AHK_NotifyTrayIcon")

Menu, Tray, Icon, %TrayIconFile%

Menu,Tray,NoStandard

return

AHK_NotifyTrayIcon(wParam, lParam) {

  If (lparam = 517)
  {
    global RunScript
    global MenuContentsFile
    RunWait, %RunScript% list 7 %MenuContentsFile%
    GoSub, ChangeMenu
  }
}

Return

ChangeMenu:

Menu,Tray,DeleteAll

day := 0
sessioncount := 0 ; num sessions in a day

Loop, read, %MenuContentsFile%
{
    line := StrSplit(A_LoopReadLine, ",")
    if (A_Index > 1 && day != line[1])
    {
    	Gosub, AddDay
	sessioncount := 0
    }
    sessioncount += 1
    day := line[1]
    start_file := line[5]
    start_time := line[2]
    num_files := line[4]
    file_string := (num_files = 1) ? "1 file" : num_files . " files"
    duration := line[3]
    bound_command := Func("OpenSession").Bind(start_file)
    Menu,%day%,Add,%start_time% - %file_string% (%duration%), % bound_command
}
Gosub, AddDay

Menu,Tray,Add

Menu,Tray,Add,Exit,Exit

Return

AddDay:
Menu, Tray, Add, %day% - %sessioncount% sessions, :%day%


Return:

Return

OpenSession(startFile)
{
    global RunScript
    global DownloadFolder
    RunWait, %RunScript% get %startFile% %DownloadFolder%

    SetTitleMatchMode, 2

    WinGet, hWnd, ID, REAPER

    WinActivate, ahk_id %hWnd%

    WinWaitActive, ahk_id %hWnd%
    
    Send, {F1}

}

Exit:

ExitApp
