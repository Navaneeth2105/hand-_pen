# Quick Start Guide

## 🚀 Get Started in 30 Seconds

### Web Version (No Installation)
```bash
# Just open the file in your browser!
open index.html    # macOS
# or right-click → Open with browser
```

### Python Version
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python air_mouse.py

# 3. Press 'q' to exit
```

---

## 🎮 Controls Quick Reference

### Web Version (index.html)
| Action | Control |
|--------|---------|
| **Draw** | Hold `SHIFT` + Move finger |
| **Move** | Release `SHIFT` + Move finger |
| **Clear** | Press `SPACE` |
| **Help** | Press `H` |
| **Debug** | Press `D` |

### Python Version (air_mouse.py)
| Action | Gesture |
|--------|---------|
| **Move Cursor** | Move index finger |
| **Click** | Pinch index + middle finger |
| **Scroll Up** | Both fingers pointing up (top of screen) |
| **Scroll Down** | Both fingers pointing up (bottom of screen) |
| **Exit** | Press `q` |

---

## 💡 Tips for Best Results

✅ **Do:**
- Use good lighting (side or front lighting works best)
- Keep your hand within the camera frame
- Move slowly for precision drawing
- Keep fingers relaxed and visible

❌ **Avoid:**
- Backlighting or shadows on your hand
- Quick jerky movements
- Covering your hand with other objects
- Poor lighting conditions

---

## 🔧 Configuration

### Adjust Drawing Smoothness (Web)
In `index.html`, find this line:
```javascript
smoothX += (rawX - smoothX) * 0.45;
```
- **Lower value** (0.2) = More responsive but jittery
- **Higher value** (0.7) = Smoother but delayed

### Adjust Mouse Sensitivity (Python)
In `air_mouse.py`, modify:
```python
smoothing = 5  # Change this value
# Lower = more responsive
# Higher = smoother movement
```

---

## 🐛 Troubleshooting

### Web Version Not Working
1. **Camera not detected?** - Check browser permissions
2. **Hand not detected?** - Improve lighting
3. **Laggy performance?** - Close other applications
4. **Try a different browser** - Chrome usually works best

### Python Version Issues
1. **ImportError for cv2?**
   ```bash
   pip install --upgrade opencv-python
   ```

2. **Camera not found?**
   - Check if another app is using the camera
   - Try restarting the computer
   - On Linux: `sudo` may be needed

3. **Permission denied?**
   - Windows: Run terminal as administrator
   - Mac/Linux: Run with `sudo python air_mouse.py`

### Poor Hand Detection
- Add more lighting
- Move hand closer to camera
- Clean camera lens
- Try in a different room

---

## 📦 System Requirements

### Web Version
- Modern browser (Chrome, Firefox, Safari, Edge)
- Webcam
- **No installation needed!**
- ~10 MB internet for libraries (one-time)

### Python Version
- Python 3.8+
- Pip package manager
- Webcam
- 200 MB free disk space
- Windows, macOS, or Linux

---

## 🎯 Common Use Cases

- **Digital Art**: Create digital drawings
- **Note-taking**: Hand-written notes digitally
- **Presentations**: Gesture-based pointer
- **UI Control**: Hands-free interface control
- **Games**: Gesture-based game control

---

## 📞 Need Help?

1. Check the README.md for detailed documentation
2. Review troubleshooting section above
3. Check hand detection - press 'H' for debug info
4. Ensure good lighting conditions

---

## 📝 Version Info

**Hand Pen v1.0.0**
- Web: index.html
- Python: air_mouse.py
- Requirements: requirements.txt
- Documentation: README.md

Enjoy! 🖋️✨
