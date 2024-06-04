import ctypes
from ctypes import wintypes


# Define the MARGINS structure
class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int)]


# Constants
WS_EX_LAYERED = 0x00080000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_TOPMOST = 0x00000008
WS_EX_TRANSPARENT = 0x00000020
SW_SHOW = 5
GWL_EXSTYLE = -20
SWP_NOREDRAW = 0x0008

# Load necessary libraries
user32 = ctypes.WinDLL('user32', use_last_error=True)
dwmapi = ctypes.WinDLL('dwmapi', use_last_error=True)

# Define necessary functions
FindWindowA = user32.FindWindowA
FindWindowA.argtypes = [wintypes.LPCSTR, wintypes.LPCSTR]
FindWindowA.restype = wintypes.HWND

ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
ShowWindow.restype = wintypes.BOOL

# Define HRESULT using ctypes.c_long
HRESULT = ctypes.c_long

DwmExtendFrameIntoClientArea = dwmapi.DwmExtendFrameIntoClientArea
DwmExtendFrameIntoClientArea.argtypes = [wintypes.HWND, ctypes.POINTER(MARGINS)]
DwmExtendFrameIntoClientArea.restype = ctypes.c_long  # Correctly define HRESULT

SetWindowLongA = user32.SetWindowLongA
SetWindowLongA.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
SetWindowLongA.restype = ctypes.c_long

SetWindowPos = user32.SetWindowPos
SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                         ctypes.c_uint]
SetWindowPos.restype = wintypes.BOOL

UpdateWindow = user32.UpdateWindow
UpdateWindow.argtypes = [wintypes.HWND]
UpdateWindow.restype = wintypes.BOOL


# Function to hijack overlay
def hijack_overlay():
    overlay = FindWindowA(b"CiceroUIWndFrame", b"CiceroUIWndFrame")
    if not overlay:
        print("Failed to find overlay.")
        return False

    ShowWindow(overlay, SW_SHOW)

    margins = MARGINS(-1, -1, -1, -1)
    hr = DwmExtendFrameIntoClientArea(overlay, ctypes.byref(margins))
    if hr != 0:
        print(f"Failed to extend frame into client area. HRESULT: {hr}")
        return False

    SetWindowLongA(overlay, GWL_EXSTYLE, WS_EX_LAYERED | WS_EX_TOOLWINDOW | WS_EX_TOPMOST | WS_EX_TRANSPARENT)
    SetWindowPos(overlay, 0, 0, 0, 50, 50, SWP_NOREDRAW)  # Adjust width and height to 50x50
    UpdateWindow(overlay)

    print("Successful hijacking")
    return True


if __name__ == "__main__":
    hijack_overlay()
