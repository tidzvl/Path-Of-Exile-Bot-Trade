Local $pos_x[12] = [20, 60, 100, 140, 180, 220, 260, 300, 340, 380, 420, 460]
Local $pos_y[12] = [140, 180, 220, 260, 300, 340, 380, 420, 460, 500, 540, 580]
Local $stash[3][2] = [[560, 104], [560, 123], [560,140]]
Local $inventory_x[12] = [1080, 1120, 1160, 1200, 1240, 1280, 1320, 1360, 1400, 1440, 1480, 1520]
Local $inventory_y[5] = [470, 510, 550, 590, 630]

Func ExitProgram()
    Exit
EndFunc

HotKeySet("`", "ExitProgram")
$fileContent = FileRead("logs.txt")
$array = StringSplit($fileContent, ",")
$x = $array[1]
$y = $array[2]
$z = $array[3]
$hwnd = WinGetHandle("Path of Exile")
WinActivate($hwnd)
Sleep(100)
MouseClick("main",721,357)
Sleep(100)
MouseClick("main", $stash[$z][0], $stash[$z][1])
Sleep(100)
Send("{CTRLDOWN}")
;~ For $i = 0 To 11 Step 1
;~ 	For $j = 0 To 4 Step 1
;~ 		MouseClick("main",$inventory_x[$i],$inventory_y[$j],1,10)
;~ 		Sleep(100)
;~ 	Next
;~ Next
MouseClick("main",$pos_x[$x]+7,$pos_y[$y]-10,1,10)
Sleep(100)
Send("{CTRLUP}")