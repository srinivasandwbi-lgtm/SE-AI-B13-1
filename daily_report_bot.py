"""
daily_report_bot.py

Automates a daily weather report:
1. Opens Chrome and loads a public weather page for Chennai (wttr.in).
2. Copies the page text using the keyboard and extracts the weather summary.
3. Creates an Excel workbook with runtime date/time, fetched data, and a comment.
4. Opens the workbook in Excel (Windows) or Numbers/Excel (macOS).
5. Saves a screenshot of the open spreadsheet.

Install:
    python -m pip install pyautogui pyperclip openpyxl

Run:
    python daily_report_bot.py

Notes:
- Close any first-run Chrome/Excel dialogs before running.
- Do not move the mouse or type while the automation is running.
- On macOS, grant Accessibility and Screen Recording permissions to your
  terminal/IDE under System Settings > Privacy & Security.
"""

from __future__ import annotations

import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


# --------------------------- Configuration ---------------------------

CITY = "Chennai"
WEATHER_URL = f"https://wttr.in/{CITY}?0"
OUTPUT_DIR = Path.cwd() / "daily_report_output"
PAGE_LOAD_TIMEOUT = 45
APP_OPEN_TIMEOUT = 25
KEY_INTERVAL = 0.04

# PyAutoGUI safety: moving the mouse to the top-left corner aborts the run.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25


# --------------------------- Helper functions -------------------------

def wait_for_clipboard_change(previous: str, timeout: int = 12) -> str:
    """Wait until Ctrl+A/Ctrl+C places page text on the clipboard."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = pyperclip.paste()
        if current and current != previous:
            return current
        time.sleep(0.4)

    # Clipboard contents can be identical on repeat runs; return what is there.
    return pyperclip.paste()


def launch_chrome() -> None:
    """Open Chrome, using the platform's normal application launcher."""
    system = platform.system()

    try:
        if system == "Windows":
            # Chrome is commonly registered with the Windows start command.
            subprocess.Popen(
                ["cmd", "/c", "start", "", "chrome", WEATHER_URL],
                shell=False,
            )
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Chrome", WEATHER_URL])
        else:
            subprocess.Popen(["google-chrome", WEATHER_URL])
    except (FileNotFoundError, OSError) as exc:
        raise RuntimeError(
            "Could not launch Google Chrome. Install Chrome or update "
            "launch_chrome() with its executable path."
        ) from exc


def fetch_weather_with_browser() -> str:
    """Use PyAutoGUI to focus Chrome, navigate, and copy visible page text."""
    old_clipboard = pyperclip.paste()
    launch_chrome()

    # Allow Chrome to start, then explicitly navigate in case it opened a
    # blank/new window rather than the requested URL.
    time.sleep(4)
    pyautogui.hotkey("ctrl" if platform.system() != "Darwin" else "command", "l")
    pyautogui.write(WEATHER_URL, interval=KEY_INTERVAL)
    pyautogui.press("enter")

    # Wait for a slow connection/page load without assuming a fixed short delay.
    start = time.time()
    page_text = ""
    while time.time() - start < PAGE_LOAD_TIMEOUT:
        time.sleep(2)
        modifier = "command" if platform.system() == "Darwin" else "ctrl"
        pyautogui.hotkey(modifier, "a")
        pyautogui.hotkey(modifier, "c")
        time.sleep(0.5)
        page_text = pyperclip.paste()
        if page_text.strip() and (
            "weather" in page_text.lower()
            or "°" in page_text
            or "chennai" in page_text.lower()
        ):
            break

    if not page_text.strip():
        page_text = wait_for_clipboard_change(old_clipboard)

    if not page_text.strip():
        raise RuntimeError(
            "No page text was copied. Check Chrome focus, internet access, "
            "and clipboard permissions."
        )

    return page_text.strip()


def extract_weather_summary(page_text: str) -> str:
    """Extract a concise weather line from wttr.in text output."""
    lines = [re.sub(r"\s+", " ", line).strip()
             for line in page_text.splitlines() if line.strip()]

    # wttr.in's compact output commonly contains city, condition and temperature.
    for line in lines:
        if CITY.lower() in line.lower() and (
            "°" in line or "cloud" in line.lower()
            or "rain" in line.lower() or "clear" in line.lower()
        ):
            return line[:300]

    # Fallback: choose a short non-empty line that is not browser chrome text.
    for line in lines:
        if len(line) >= 8 and len(line) <= 300:
            return line

    return page_text[:300].replace("\n", " ")


def make_comment(weather: str) -> str:
    """Generate a simple comment from the fetched weather text."""
    lower = weather.lower()
    if any(word in lower for word in ("rain", "shower", "thunder")):
        return "Carry an umbrella; outdoor plans may be affected."
    if any(word in lower for word in ("sunny", "clear")):
        return "Generally suitable for outdoor activities; stay hydrated."
    if "cloud" in lower:
        return "Partly or mostly cloudy; check conditions before outdoor plans."
    return "Review the latest conditions before planning outdoor activities."


def create_report(weather: str) -> tuple[Path, Path]:
    """Create and format the workbook, then reserve a screenshot filename."""
    now = datetime.now().astimezone()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    date_for_filename = now.strftime("%Y-%m-%d")
    workbook_path = OUTPUT_DIR / f"daily_report_{date_for_filename}.xlsx"
    screenshot_path = OUTPUT_DIR / f"daily_report_{date_for_filename}.png"

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Daily Report"

    headers = ["Date & Time", "Fetched Information", "Comment"]
    sheet.append(headers)
    sheet.append([
        now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        weather,
        make_comment(weather),
    ])

    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for cell in sheet[2]:
        cell.alignment = Alignment(vertical="top", wrap_text=True)

    widths = [25, 58, 65]
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width

    sheet.row_dimensions[1].height = 24
    sheet.row_dimensions[2].height = 48
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = "A1:C2"

    workbook.save(workbook_path)
    return workbook_path, screenshot_path


def open_spreadsheet(path: Path) -> None:
    """Open the generated .xlsx file in the system's spreadsheet app."""
    system = platform.system()
    if system == "Windows":
        os.startfile(str(path))  # Opens in the default app, normally Excel.
    elif system == "Darwin":
        # Prefer Excel if installed; otherwise macOS opens it in Numbers.
        try:
            subprocess.Popen(["open", "-a", "Microsoft Excel", str(path)])
        except OSError:
            subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])

    time.sleep(APP_OPEN_TIMEOUT)


def save_spreadsheet_screenshot(path: Path) -> None:
    """Capture the screen after the spreadsheet has opened."""
    # A short settling delay allows the spreadsheet window to render.
    time.sleep(3)
    image = pyautogui.screenshot()
    image.save(path)


# -------------------------------- Main ---------------------------------

def main() -> int:
    print("Starting Daily Report Bot...")
    print(f"Weather source: {WEATHER_URL}")

    try:
        weather_page = fetch_weather_with_browser()
        weather_summary = extract_weather_summary(weather_page)
        print(f"Fetched information: {weather_summary}")

        workbook_path, screenshot_path = create_report(weather_summary)
        print(f"Excel report saved: {workbook_path}")

        open_spreadsheet(workbook_path)
        save_spreadsheet_screenshot(screenshot_path)

        print(f"Screenshot saved: {screenshot_path}")
        print("Daily report completed successfully.")
        return 0

    except pyautogui.FailSafeException:
        print("Automation stopped by PyAutoGUI fail-safe (mouse moved to top-left).")
        return 2
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
