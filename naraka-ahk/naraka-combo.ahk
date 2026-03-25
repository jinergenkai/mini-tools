; AutoHotkey v2
#Requires AutoHotkey v2.0
#SingleInstance Force
SendMode "Event"  ; Đổi sang Event để bypass game detection
SetWorkingDir A_ScriptDir

; ================================
; KIỂM TRA VÀ YÊU CẦU ADMIN
; ================================
if not A_IsAdmin {
    try {
        if A_IsCompiled
            Run '*RunAs "' A_ScriptFullPath '" /restart'
        else
            Run '*RunAs "' A_AhkPath '" /restart "' A_ScriptFullPath '"'
    }
    ExitApp
}

; ================================
; NARAKA COMBO SCRIPT
; ================================
; Hotkey: XButton1 (Nút dưới side chuột)
; Action: Giữ Shift+S, sau delay thì C + chuột phải
; ================================

; Cấu hình thời gian (milliseconds)
delayBeforeAction := 200  ; Thời gian chờ trước khi C
delayAfterC := 1     ; Thời gian giữa C và chuột phải

; Hotkey: XButton1 (nút dưới side chuột)
XButton1:: {
    ; Giữ Shift+S xuống
    Send "{Shift down}{a down}"

    Sleep delayBeforeAction

    Send "c"
    Sleep delayAfterC

    Send "{a up}{Shift up}"

    SendEvent "{RButton down}"
    Sleep 1
    SendEvent "{RButton up}"

}

; Nhấn F1 để reload script
F1::Reload

; Nhấn F2 để tạm dừng/tiếp tục script
F2::Suspend