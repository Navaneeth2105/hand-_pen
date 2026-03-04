# Development Guide

## Project Structure

```
hand-pen/
├── index.html          # Web-based drawing app
├── air_mouse.py        # Python desktop mouse controller
├── requirements.txt    # Python dependencies
├── README.md          # Main documentation
├── QUICKSTART.md      # Quick start guide
├── DEVELOPMENT.md     # This file
└── .gitignore         # Git ignore rules
```

---

## Architecture

### Web Version (`index.html`)

**Flow:**
1. Camera input → MediaPipe Hands → Hand landmarks
2. Process index finger position → Apply smoothing
3. Detect SHIFT key → Enter drawing mode
4. Store strokes in memory → Render to canvas
5. Display hand skeleton + cursor position

**Key Components:**
- **MediaPipe Hands**: Hand detection and tracking
- **Canvas API**: Drawing and rendering
- **Keyboard Events**: Input handling
- **FPS Counter**: Performance monitoring

**Technologies:**
- HTML5 Canvas
- JavaScript (ES6+)
- MediaPipe JS SDK
- No external dependencies (pure JS)

### Python Version (`air_mouse.py`)

**Flow:**
1. Webcam input → OpenCV capture
2. Convert BGR → RGB color space
3. Process with MediaPipe Hands
4. Extract landmarks → Calculate distances
5. Detect gestures → Control mouse/scroll
6. Apply smoothing → Move cursor

**Key Components:**
- **HandMouseController**: Main controller class
- **Gesture Detection**: Click, scroll, movement
- **Screen Mapping**: Coordinate transformation
- **Smoothing**: Exponential moving average

**Technologies:**
- OpenCV (cv2)
- MediaPipe
- PyAutoGUI
- NumPy

---

## Configuration

### Web Version

**Smoothing Factor** (`CONFIG.smoothing`)
```javascript
CONFIG.smoothing = 0.45;  // 45% interpolation
// Higher = smoother but more delayed
// Lower = more responsive but jittery
```

**Pen Appearance** (`CONFIG`)
```javascript
CONFIG.penColor = '#F5D061';      // Pen color
CONFIG.penWidth = 6;               // Stroke thickness
CONFIG.shadowBlur = 15;            // Glow effect
CONFIG.canvasOpacity = 0.85;       // Background fade
```

**Detection Settings**
```javascript
CONFIG.minDetectionConfidence = 0.5;
CONFIG.minTrackingConfidence = 0.5;
// 0.0-1.0: Higher = stricter detection
```

### Python Version

**Smoothing** (`CONFIG['smoothing']`)
```python
CONFIG['smoothing'] = 5  # Movement smoothing
# Higher = smoother
# Lower = more responsive
```

**Gesture Detection** (`CONFIG`)
```python
CONFIG['click_distance_threshold'] = 40      # Pinch sensitivity
CONFIG['double_click_delay'] = 0.2          # Click delay
CONFIG['scroll_cooldown'] = 0.1             # Scroll rate limit
```

---

## Extending the Project

### Adding New Gestures (Web)

**Example: Two-finger swipe to erase**

```javascript
// In drawCanvas function, after hand detection:
const index = lm[8];
const middle = lm[12];
const distance = Math.hypot(
    (index.x - middle.x) * canvas.width,
    (index.y - middle.y) * canvas.height
);

if (distance < 30 && isSwipeDown) {
    // Erase logic
    strokes.pop();
}
```

### Adding New Gestures (Python)

**Example: Three-finger tap for undo**

```python
def handle_three_finger_tap(self, landmarks):
    """Detect three-finger tap."""
    index = landmarks[8]
    middle = landmarks[12]
    ring = landmarks[16]
    
    dist_im = self.calculate_distance(index, middle, w, h)
    dist_mr = self.calculate_distance(middle, ring, w, h)
    
    if dist_im < 30 and dist_mr < 30:
        print("Three-finger tap detected")
        # Implement undo logic
```

### Adding Debug Visualization

**Web:**
```javascript
// Draw detection box
ctx.strokeStyle = '#FF0000';
ctx.strokeRect(landmark.x * canvas.width - 5, 
               landmark.y * canvas.height - 5, 10, 10);
```

**Python:**
```python
# Draw landmarks on frame
cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
cv2.putText(frame, f"({x}, {y})", (int(x), int(y)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

---

## Performance Optimization

### Web Version

1. **Canvas Rendering**
   - Use `requestAnimationFrame` for smooth updates
   - Batch draw operations
   - Limit stroke history size

2. **Hand Detection**
   - Reduce model complexity: `modelComplexity: 0` (lite)
   - Lower detection confidence threshold
   - Process every other frame: `setInterval(..., 33)`

3. **Memory Management**
   - Clear old strokes periodically
   - Limit max strokes: `if (strokes.length > 1000) strokes.shift()`
   - Use typed arrays for coordinates

### Python Version

1. **Frame Processing**
   - Skip frames: `if frame_count % 2 == 0: process()`
   - Lower resolution: `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)`

2. **Detection**
   - Reduce model complexity
   - Increase min_detection_confidence
   - Process ROI only

3. **Display**
   - Reduce window size
   - Limit FPS: `time.sleep(0.033)` for 30 FPS

---

## Testing

### Web Version

**Manual Testing Checklist:**
- [ ] Hand detection works in various lighting
- [ ] Drawing is smooth and responsive
- [ ] SHIFT key toggles draw mode
- [ ] SPACE clears canvas
- [ ] H key shows/hides help
- [ ] FPS counter updates
- [ ] Hand skeleton draws correctly
- [ ] Works on mobile browsers

### Python Version

**Testing:**
```bash
# Debug mode
python -c "
from air_mouse import HandMouseController
import logging
logging.basicConfig(level=logging.DEBUG)
controller = HandMouseController()
controller.run()
"

# Check dependencies
python -m pip check

# Test imports
python -c "import cv2, mediapipe, pyautogui; print('✅ All imports OK')"
```

---

## Common Modifications

### Change Pen Color

**Web:**
```javascript
CONFIG.penColor = '#FF0000';  // Red
ctx.strokeStyle = CONFIG.penColor;
```

**Visual Feedback:**
```html
<!-- Add color picker to HTML -->
<input type="color" id="colorPicker" value="#F5D061">
<script>
    document.getElementById('colorPicker').addEventListener('change', (e) => {
        CONFIG.penColor = e.target.value;
    });
</script>
```

### Add Pressure Sensitivity

**Web:**
```javascript
// Use hand size as "pressure"
const handSize = Math.hypot(
    (lm[0].x - lm[20].x) * canvas.width,
    (lm[0].y - lm[20].y) * canvas.height
);
ctx.lineWidth = handSize / 50;  // Dynamic thickness
```

### Add Save/Export

**Web:**
```javascript
function exportDrawing() {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'drawing.png';
    link.click();
}
```

---

## Debugging Tips

### Web Version

```javascript
// Log hand landmarks
if (landmarks) {
    console.log('Index finger:', landmarks[8]);
    console.log('All landmarks:', landmarks);
}

// Visual debug overlay
ctx.strokeStyle = '#FF0000';
for (let i = 0; i < landmarks.length; i++) {
    const x = landmarks[i].x * canvas.width;
    const y = landmarks[i].y * canvas.height;
    ctx.strokeRect(x - 2, y - 2, 4, 4);
}

// Performance profiling
console.time('drawCanvas');
drawCanvas(image, landmarks);
console.timeEnd('drawCanvas');
```

### Python Version

```python
# Enable debug mode
CONFIG['debug_mode'] = True

# Print hand position
print(f"Cursor: ({cursor_x:.1f}, {cursor_y:.1f})")

# Log gestures
print(f"Click distance: {distance:.1f}")
print(f"Scroll detected: {index_finger.y}")

# Profile performance
import cProfile
cProfile.run('controller.run()')
```

---

## Contributing Guidelines

1. **Code Style**
   - Follow PEP 8 for Python
   - Use consistent formatting
   - Add comments for complex logic

2. **Testing**
   - Test on multiple devices
   - Verify gesture recognition
   - Check performance

3. **Documentation**
   - Update README for new features
   - Add docstrings to functions
   - Include usage examples

4. **Commits**
   - Clear commit messages
   - Reference issues when applicable
   - One feature per commit

---

## Build & Deploy

### Web Version

**Local Testing:**
```bash
# Option 1: Python server
python -m http.server 8000
# Open: http://localhost:8000/index.html

# Option 2: Live Server (VS Code)
# Install "Live Server" extension
# Right-click → "Open with Live Server"
```

**Deploy:**
- Upload to GitHub Pages
- Deploy to Vercel, Netlify, or GitHub Pages
- No build process needed!

### Python Version

**Package for Distribution:**
```bash
# Create executable (Windows)
pip install pyinstaller
pyinstaller --onefile --windowed air_mouse.py

# Create wheel
pip install wheel
python setup.py bdist_wheel
```

---

## Resources

- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Canvas API Docs](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)

---

## License

This project is open source. Feel free to fork, modify, and use!

---

**Last Updated**: 2024
**Version**: 1.0.0
