
# RP2040 OLED Macro Pad & Media Controller

A custom programmable 3x3 mechanical keyboard macro pad powered by a Raspberry Pi Pico (RP2040). It features a rotary encoder for volume control and an OLED display that dynamically updates to show the current key bindings.

## Features

*   **3 Programmable Layers (Profiles):**
    1.  **Web & Apps:** Shortcuts for YouTube, GitHub, Netflix, Gmail, etc.
    2.  **Media Control:** Play/Pause, Previous/Next, and Arrow navigation.
    3.  **Productivity:** Select All, Undo, Redo, and Math equation shortcuts (Superscript/Subscript).
*   **OLED Status Display:** A 128x64 SSD1306 display shows a 3x3 grid of labels corresponding to the active layer.
*   **Rotary Encoder:** Dedicated volume knob (CW/CCW) with Mute function (Click).
*   **Layer Switching:** Dedicated key (Bottom Right) to cycle through profiles.
*   **OS Support:** Optimised for **Windows** (uses `Win+R` for URL launching and Windows Search for apps).

## Usage

### Profile Navigation
The matrix is arranged as:
```text
[1] [2] [3]
[4] [5] [6]
[7] [8] [9]
```
**Key 9** (Bottom Right) is the **Profile Switcher**. Pressing it cycles through Profile 0 -> 1 -> 2 -> 0.

### Profile 0: Web & Apps
*   **1:** Open YouTube
*   **2:** Open Google AI Studio
*   **3:** Open LMS
*   **4:** Open GitHub
*   **5:** Open HBO Max
*   **6:** Open Gmail
*   **7:** Open Netflix App
*   **8:** Open Whatsapp App
*   **9:** *Next Profile*

### Profile 1: Media Control
*   **1:** Previous Track
*   **2:** Left Arrow
*   **4:** Stop
*   **5:** Play/Pause
*   **7:** Next Track
*   **8:** Right Arrow
*   **3 & 6:** (Unused)
*   **9:** *Next Profile*

### Profile 2: Productivity
*   **1:** Select All (`Ctrl+A`)
*   **2:** Insert Equation (`Alt+=`)
*   **4:** Undo (`Ctrl+Z`)
*   **5:** Superscript (`Ctrl+Shift+=`)
*   **7:** Redo (`Ctrl+Y`)
*   **8:** Subscript (`Ctrl+Shift+-`)
*   **3 & 6:** (Unused)
*   **9:** *Next Profile*

### Rotary Encoder
*   **Rotate CW:** Volume Up
*   **Rotate CCW:** Volume Down
*   **Press:** Mute/Unmute


## Customization - In Development

To change the links or key bindings, edit the `code.py` file:
1.  Look for `profile_0_actions` dictionary to change URLs.
2.  Look for the `box` list to change the text displayed on the OLED screen.