# overlay-hijacking

Overlay Hijacking Tool
This repository contains a Python script designed to hijack and modify the properties of a specific overlay window on Windows systems. The script uses the ctypes library to interact with Windows API functions, allowing it to find, show, and modify the overlay window's properties to achieve a "sheet of glass" effect.

Features
Find and Modify Overlay Window: The script locates the overlay window with the class name "CiceroUIWndFrame" and modifies its properties.
Extend Frame into Client Area: Uses the DwmExtendFrameIntoClientArea function to extend the frame into the client area with negative margins.
Set Window Properties: Adjusts the window's extended style to be layered, a tool window, topmost, and transparent.
Position and Size Adjustment: Sets the window's position and size to specified dimensions.
Debug Information: Outputs debug information to the console to verify the success of the hijacking process.
