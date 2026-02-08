# Vehicle Plate Detection & Pollution Lookup

A web app that detects license plate regions in images and looks up vehicle pollution data by plate number.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python backend.py
```

Then open **http://localhost:5000** in your browser.

## Features

- **Plate Detection**: Upload an image to detect and highlight the license plate region using OpenCV
- **Pollution Lookup**: Enter a plate number to get CO₂, NOx, and PM2.5 emissions plus pollution classification

### Demo plates

- `MH12AB1234` - High pollution
- `DL9CG4545` - Moderate pollution  
- `KA05AB6789` - Low pollution

<img width="1562" height="705" alt="image" src="https://github.com/user-attachments/assets/7bc462b6-8cd3-4292-8ec4-a8f6e30c88f8" />
