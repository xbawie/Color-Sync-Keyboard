# ⚡ Lumina RGB Studio Pro

> A modern, lightweight, high-performance desktop screen ambience synchronization engine for OpenRGB-compatible keyboards.

![Python](https://img.shields.io/badge/Python-3.9%2B-06B6D4?style=for-the-badge&logo=python&logoColor=white)
![OpenRGB](https://img.shields.io/badge/OpenRGB-Supported-8B5CF6?style=for-the-badge)
![Instagram](https://img.shields.io/badge/Created%20By-@matei.tem-E4405F?style=for-the-badge&logo=instagram&logoColor=white)

---

## ✨ Features

- **🖥️ Screen Ambience Sync**: Real-time 1x1 downsampled color extraction for minimal CPU overhead.
- **🎨 Color Tuning**: Dynamic saturation boosting ($1.0x - 4.0x$) and brightness controls ($0.5x - 2.0x$).
- **💧 Fluid Color Interpolation**: Built-in color smoothing engine to prevent harsh, jumpy lighting shifts.
- **🖥️ Multi-Monitor Support**: Switch target screens seamlessly on the fly.
- **⚡ High FPS Control**: Configurable update rate from 15 FPS up to 60 FPS.
- **🔌 Automatic OpenRGB Detection**: Re-scan connected hardware targets with a single click.

---

## 🚀 Quick Start

### 1. Prerequisites
- Install and launch [OpenRGB](https://openrgb.org/).
- Go to the **SDK Server** tab inside OpenRGB and click **Start Server**.

### 2. Installation & Running

```bash
# Clone this repository
git clone [https://github.com/YOUR_USERNAME/Lumina-RGB-Studio.git](https://github.com/YOUR_USERNAME/Lumina-RGB-Studio.git)
cd Lumina-RGB-Studio

# Install dependencies
pip install -r requirements.txt

# Run the app
python keyboardRGB.py
