# 🎹 Invisible MIDI Instrument

A touchless, Arduino-based MIDI controller that uses infrared (IR) proximity sensors and gesture recognition to control musical notes and expressions in real-time—no physical keys required.

---

## 📌 Overview

This project demonstrates a **contactless digital instrument** powered by:

- 🎵 **MIDI over serial** via Arduino UNO R4
- ✋ **Infrared proximity sensors** as virtual keys
- 👆 **Gesture recognition** using MediaPipe for volume and mode control
- 🎚️ **Push button** for real-time instrument switching (drums, piano, etc.)
- 💻 Compatibility with popular software synthesizers (VMPK, Sforzando, CoolSoft, etc.)

Designed for accessibility, performance, education, and experimentation.

---

## ⚙️ Hardware Components

- Arduino UNO R4
- 10× IR Proximity Sensors (e.g., TCRT5000)
- 1× Push Button
- USB Cable
- Jumper Wires and Breadboard (optional)

---

## 💽 Software Requirements

### Arduino Side
- Arduino IDE
- Hairless MIDI Serial Bridge (for MIDI over USB)
- LoopMIDI (for virtual MIDI port)

### Python Side (Gesture Recognition)
- Python 3.7+
- Dependencies in `requirements.txt`

```bash
pip install -r requirements.txt
