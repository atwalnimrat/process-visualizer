## Process Visualizer

A frameless, transparent GUI application to visualize processes in real-time, built with Python. It features a system stats (CPU usage, memory usage, CPU temperature) visualizer which is toggable using a button. Designed for all desktop environments.

---

## Features

* Frameless, transparent window interface for unobtrusive visualization
* Real-time process monitoring
* Real-time CPU usage, CPU temperature and memory usage graphs
* Lightweight and minimal UI
* Can be set to auto-start on login in Fedora GNOME

---

## Requirements

* Python 3.10+
* Dependencies listed in `requirements.txt` 

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the App

From the project root directory, run:

```bash
python -m gui.main
```

Your frameless transparent window should appear.

---
To view the cli prototype, run the following from the root directory:

```bash
python -m cli.main
```

---

## Making It Run on Startup (Fedora GNOME)

To launch Process Visualizer automatically when you log in:

1. **Create the autostart directory** (if it doesn’t exist):

```bash
mkdir -p ~/.config/autostart
```

2. **Create a `.desktop` file**:

```bash
nano ~/.config/autostart/pv.desktop
```

3. **Add the following content** (update paths as necessary):

```ini
[Desktop Entry]
Type=Application
Name=ProcessVisualizer
Comment=Startup frameless app
Exec=bash -c "cd /path/to/project && /usr/bin/python3 -m gui.main"
X-GNOME-Autostart-enabled=true
```

4. **Make the file executable**:

```bash
chmod +x ~/.config/autostart/pv.desktop
```

Process Visualizer will now automatically launch at login.

---

## Troubleshooting

* **ModuleNotFoundError: No module named 'gui'**
  Ensure the `Exec` command runs from the project root directory using `cd /path/to/project`.

* **App doesn’t start at login**
  GNOME may launch apps too early; add a delay in the `.desktop` file:

```ini
Exec=bash -c "sleep 10 && cd /path/to/project && /usr/bin/python3 -m gui.main"
```

* **Terminal window flashes or appears briefly**
  This is normal when running a Python script directly. Packaging into an executable can remove the terminal window.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with improvements or bug fixes.

