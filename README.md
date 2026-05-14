# Hand Pen 🖋️

A modern gesture-controlled virtual drawing and air interaction application powered by computer vision and real-time hand tracking.

Hand Pen allows users to draw, interact, and control digital actions using only hand gestures captured through a webcam. The project includes both a web-based implementation and a Python desktop version.

---

## 🚀 Features

- ✋ Real-time hand tracking using MediaPipe
- 🎨 Virtual air drawing with smooth strokes
- 🖱️ Gesture-based mouse interaction
- ✨ Glow effects and visual feedback
- 📷 Live webcam hand visualization
- ⚡ Lightweight and fast performance
- 🌐 Web version with zero installation
- 🐍 Python desktop version for advanced controls

---

## 🛠️ Tech Stack

### Web Version
- HTML5
- CSS3
- JavaScript
- MediaPipe Hands API
- Canvas API

### Python Version
- Python 3.8+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

---

## 📂 Project Structure

```bash
hand-_pen/
│
├── index.html        # Web-based hand drawing app
├── air_mouse.py      # Python gesture mouse controller
├── README.md
```

---

## 🌐 Web Version Setup

No installation required.

### Steps

1. Open `index.html` in a modern browser
2. Allow webcam access
3. Use hand gestures to draw

### Controls

| Key | Action |
|------|---------|
| SHIFT | Hold to draw |
| SPACE | Clear canvas |
| C | Toggle cursor |
| Q | Exit/Stop |

---

## 🐍 Python Version Setup

### Requirements

- Python 3.8 or later
- Webcam access

### Installation

```bash
pip install opencv-python mediapipe pyautogui numpy
```

### Run the Application

```bash
python air_mouse.py
```

### Gesture Controls

| Gesture | Action |
|----------|---------|
| Index finger movement | Move cursor |
| Index + Middle finger pinch | Click |
| Two fingers vertical movement | Scroll |

---

## ⚙️ How It Works

1. Webcam captures live video frames
2. MediaPipe detects hand landmarks
3. Finger positions are tracked in real time
4. Gestures are interpreted into actions
5. Drawing or cursor movement is rendered instantly

---

## 📸 Applications

- Virtual whiteboard
- Touchless interaction systems
- Presentation control
- Gesture-based UI experiments
- Educational demos
- Fun creative drawing experiences

---

## 📈 Performance

- Real-time gesture tracking
- Low latency interaction
- Smooth drawing interpolation
- Cross-platform compatibility

---

## 🧩 Future Improvements

- Multi-hand support
- AI gesture customization
- Shape recognition
- Save/export drawings
- Mobile compatibility
- Voice + gesture integration

---

## 🤝 Contributing

Contributions are welcome.

If you'd like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

Developed by Navaneeth K.

GitHub: https://github.com/Navaneeth2105

---

## ⭐ Support

If you like this project, consider giving it a star on GitHub.
