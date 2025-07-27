# 🎹 Invisible MIDI Instrument – Touchless Virtual Piano & Synth Controller 🤖🎶

**Invisible MIDI Instrument** is a touchless, Arduino-powered MIDI controller that enables users to play musical notes and switch instruments in real time using IR proximity sensors and a gesture-based interface. Designed for accessibility, education, and expressive digital performances.

---

## 🌐 Demo Video & Showcase

- 🎬 **Implementation Video Demonstration**: https://drive.google.com/file/d/1_DCrn2rYo8GHHWHBQtYG0IISiD0iFFea/view?usp=drive_link
**Open CV Video Demonstration**: https://drive.google.com/file/d/1fRu_DPyqV8VpqjAnLNWHHTMdxc2kJyTc/view?usp=drive_link
- 📘 **Patent/Documentation**: _[Add link to patent doc or project report]_

---

## 🚀 Features

- 🎵 Play notes without touching – just place your hand over IR sensors  
- ✋ Gesture-based volume control using MediaPipe (up/down swipe)  
- 🔁 Push button to switch instruments on the fly (e.g., piano, drums)  
- 🎧 MIDI output via USB to software synthesizers like VMPK, Sforzando  
- 🔌 Compatible with any DAW using virtual ports (Hairless + loopMIDI)

---

## 🛠️ Tech Stack

**Hardware:**  
- Arduino UNO R4  
- IR Proximity Sensors (e.g., TCRT5000)  
- Push Button  
- Breadboard, USB Cable

**Software & Tools:**  
- Arduino IDE  
- Hairless MIDI Serial Bridge  
- loopMIDI  
- Python (for gesture control)  
- MediaPipe + PyAutoGUI  
- MIDI Synthesizer (VMPK / Sforzando / Cakewalk)

---

## 🧪 System Architecture

```text
[IR Sensors] ---> [Arduino UNO R4] ---> [Hairless MIDI + loopMIDI] ---> [Virtual Synth Software]
                           ↑
              [Gesture Control (Python)] -- Adjusts Volume / Mode

