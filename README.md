
# **.devPAD**

An Elevated "SteamDeck" for developpers with fully customizable controls across many programs. I made it to make my life easier by having all of the most used tools and a way to properly move in CAD using the joystick in the middle. The e-ink screen is used as clock and a to-do list and could display the current media, volume level, microphone status and temperature.


***the tech stack***

![Python](https://shields.io/badge/Python-yellow) 

![CPP](https://shields.io/badge/CPP-green)

![Fusion360](https://shields.io/badge/Fusion360-orange)

![KiCAD](https://shields.io/badge/KiCAD-blue)



## Screenshots


![Render](https://raw.githubusercontent.com/fayekdev/HackPad/2263917d25760ceed66eaa927af2d2fddac82332/Screenshots/.devPAD%20assembly%20v13.png)



![Physical](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/IMG_1689.jpeg)





## *THE CODE*

The code is still incomplete but still has ~80% functionality(only a few minor changes to make)

Currently working on the hardware problems so it is on delay







## *How was it made*  

- I designed the PCB in KiCAD and exported to Fusion to model the Case.

- The case was modeled and the components too to ensure the fit is correct

- Printed the first version 

- Fixed the errors in V1 and added a few features. 

- The PCB arrived and all components were test fit

- Began soldering the PCB 

- Fixed the errors I had made and uploaded a few test sketches.

- Test sketches were success and I tested the production code

- Production code worked out fine with a few problems

- A wire connected the screen to the microcontroller snapped and when trying to fix it a short-circuit happened and probably caused the microcontroller to malfunction.

*(The device only worked for 30 minutes or so before breaking)*


## *AI disclosure*

- AI was used as a research tool where I gave it all my requirements in one and it generated some sort of documentation that was held in it's context window so that when I ask a question or have a concern it automatically gives the answer I need instead of losing a ton of time researching myself

- Another usecase is the few errors I stumble upon that I spent a ton of time trying to fix I give to AI to give me a suggestion on how to fix it 

## Installation

Install the .devPAD desktop app --> 

[![Install](https://img.shields.io/badge/Install-here-blue)](https://github.com/fayekdev/HackPad/releases/tag/pre-release)


Upload the **main.ino** sketch to the microcontroller



**SCREENSHOTS OF THE APP**

![APP](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/Screenshot%202026-08-12%20094004.png)

![APP](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/Screenshot%202026-08-12%20094027.png)

![APP](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/Screenshot%202026-08-12%20094039.png)

![APP](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/Screenshot%202026-08-12%20102328.png)

![APP](https://raw.githubusercontent.com/fayekdev/HackPad/refs/heads/master/Screenshots/Screenshot%202026-08-12%20102339.png)

## BOM


| Component    | Qty |
| ---------    | --: |
|Xiao ESP32 C3                              |   1  |
|  Keycaps                                  |  14  |
|We-Act studio 2.9" E-ink screen             |   1  |
| M2x6 screws                               |   8  |
|MX-Cherr Keyswitches                       |    14  |
|     1N4148 diodes       |  16   |
|    Rotary encoder          |  1   |
|   Joystick           |   1  |
|     Wire         |   (as much as you need)  |
|    SN74HC595N          |  1   |
|PCB|  1|

**TOOLS**

- Access to a 3D printer & filament
- Soldering tools 
- Wire strippers
- USB-C wire
- Arduino IDE






## Assembly GUIDE

1. Print all of the components. The face plate cover is optional (you should glue it if you want to use it)
---
2. Solder the first diode (under the joystick) upside down then solder the rest upright.
---
3. Solder the Joystick in its respective place but make sure it is properly level.
---
4. Solder the SN74HC595 and the Xiao ESP32 C3.
---
5. Solder all of the keyswitches.
---
7. Screw in the encoder and seat in the screen (if you want to make sure it's even more secure, use some tape instead of using the support beam).
---
8. Solder all of the encoder wires from the bottom and solder them to the encoder.
---
9. Solder the screen using it's respective connections using the 
schematic as a reference PS: The purple wire is not needed and the orange one should be wired up to the RST switch.
---
10. Seat the PCB and screw it in.
---
11. Close up the top plate being careful that the wires don't interfere with the USB port. You could put the USB-C wire in and close up the top plate to keep the wires from interfering
---
12. Add the joystick, the encoder knob and the 14 keycaps.
---
13. Upload the **main.ino** sketch via the Arduino IDE and run the ".devPAD" app
---
