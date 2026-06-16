"""
One-click system setup for battery testing.

Automates the subset of the pre-test checklist that can be set reliably and
without admin/sudo on a modern machine. Anything that can't be scripted on a
given OS is reported as "skipped" so the user can still set it manually.

Each action returns a (status, message) tuple where status is one of:
    "ok"      - applied successfully
    "skip"    - not automatable on this OS (do it manually)
    "warn"    - attempted but failed

`optimize_system()` returns {action_key: (status, message)} so the GUI can
auto-tick the boxes it handled and leave the rest to the user.
"""
import logging
import platform
import subprocess


def _run(cmd):
    """Run a command, raising on non-zero exit. Output is captured/silenced."""
    subprocess.run(cmd, capture_output=True, check=True)


# --------------------------------------------------------------------------- #
# macOS
# --------------------------------------------------------------------------- #
def _set_macos_brightness(level=0.75):
    """Set built-in display brightness via the private DisplayServices API.

    Returns True on success. No AppleScript fallback by design - this targets
    modern Macs where DisplayServices is available.
    """
    import ctypes
    import ctypes.util

    cg_path = ctypes.util.find_library("CoreGraphics")
    if not cg_path:
        return False
    cg = ctypes.CDLL(cg_path)
    cg.CGMainDisplayID.restype = ctypes.c_uint32
    main_display = cg.CGMainDisplayID()

    ds = ctypes.CDLL(
        "/System/Library/PrivateFrameworks/DisplayServices.framework/DisplayServices"
    )
    ds.DisplayServicesSetBrightness.argtypes = [ctypes.c_uint32, ctypes.c_float]
    ds.DisplayServicesSetBrightness.restype = ctypes.c_int
    return ds.DisplayServicesSetBrightness(main_display, ctypes.c_float(level)) == 0


def _optimize_macos():
    results = {}

    # 1. Power mode - High Performance is off by default; nothing safe to script.
    results["power_mode"] = ("skip", "High Performance is off by default - verify manually")

    # 2. Brightness 75%
    try:
        if _set_macos_brightness(0.75):
            results["brightness"] = ("ok", "Set screen brightness to 75% (DisplayServices)")
        else:
            results["brightness"] = ("warn", "DisplayServices call failed - set 75% manually")
    except Exception as e:
        results["brightness"] = ("warn", f"Could not set brightness: {e} - set 75% manually")

    # 3. No screen-off on battery -> prevent display sleep with caffeinate.
    #    Spawned detached; it lives for the duration of the test process tree.
    try:
        subprocess.Popen(
            ["caffeinate", "-d"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        results["screen_off"] = ("ok", "Display sleep prevented (caffeinate -d running)")
    except Exception as e:
        results["screen_off"] = ("warn", f"Could not start caffeinate: {e}")

    # 4. Battery saver @ 30% - not configurable on macOS.
    results["battery_saver"] = ("skip", "Low Power threshold is not configurable on macOS")

    # 5. Lower brightness on low battery - not scriptable on macOS.
    results["low_batt_brightness"] = ("skip", "Not scriptable on macOS - verify manually")

    # 6. Volume 0%
    try:
        _run(["osascript", "-e", "set volume output volume 0"])
        results["volume"] = ("ok", "Set volume to 0%")
    except Exception as e:
        results["volume"] = ("warn", f"Could not set volume: {e}")

    return results


# --------------------------------------------------------------------------- #
# Windows
# --------------------------------------------------------------------------- #
def _set_windows_brightness(level=75):
    """Set internal-panel brightness via CIM, falling back to legacy WMI."""
    try:
        cmd = (
            "Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods "
            "| Invoke-CimMethod -MethodName WmiSetBrightness "
            f"-Arguments @{{Timeout=1; Brightness={level}}}"
        )
        _run(["powershell", "-Command", cmd])
        return True
    except Exception:
        cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})"
        _run(["powershell", "-Command", cmd])
        return True


def _optimize_windows():
    results = {}

    # 1. Power mode -> Balanced plan (GUID 381b4222-...).
    try:
        _run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"])
        results["power_mode"] = ("ok", "Set power plan to Balanced")
    except Exception as e:
        results["power_mode"] = ("warn", f"Could not set Balanced plan: {e}")

    # 2. Brightness 75% (internal panel only).
    try:
        _set_windows_brightness(75)
        results["brightness"] = ("ok", "Set screen brightness to 75%")
    except Exception as e:
        results["brightness"] = ("warn", f"Could not set brightness: {e} - set 75% manually")

    # 3. No screen-off on battery.
    try:
        _run(["powercfg", "/change", "monitor-timeout-dc", "0"])
        results["screen_off"] = ("ok", "Disabled screen auto turn-off on battery")
    except Exception as e:
        results["screen_off"] = ("warn", f"Could not disable screen timeout: {e}")

    # 4. Battery saver @ 30%.
    try:
        _run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_ENERGYSAVER", "ESBATTTHRESHOLD", "30"])
        _run(["powercfg", "/setactive", "SCHEME_CURRENT"])
        results["battery_saver"] = ("ok", "Set Battery Saver to turn on at 30%")
    except Exception as e:
        results["battery_saver"] = ("warn", f"Could not set Battery Saver threshold: {e}")

    # 5. Turn "lower brightness on low battery" off (no dimming -> 100%).
    try:
        _run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_ENERGYSAVER", "ESBRIGHTNESS", "100"])
        _run(["powercfg", "/setactive", "SCHEME_CURRENT"])
        results["low_batt_brightness"] = ("ok", "Disabled 'lower brightness on low battery'")
    except Exception as e:
        results["low_batt_brightness"] = ("warn", f"Could not disable low-battery dimming: {e}")

    # 6. Volume 0% - tap the mute key.
    try:
        cmd = "$w = New-Object -ComObject Wscript.Shell; $w.SendKeys([char]173)"
        _run(["powershell", "-Command", cmd])
        results["volume"] = ("ok", "Muted system volume")
    except Exception as e:
        results["volume"] = ("warn", f"Could not set volume: {e}")

    return results


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def optimize_system(log=None):
    """Apply the automatable checklist items for the current OS.

    Args:
        log: optional callable(str) for surfacing progress (e.g. a GUI signal).
             Messages are always written to the log file and stdout regardless.

    Returns:
        dict mapping action key -> (status, message).
    """
    def emit(msg):
        print(msg)
        logging.info(msg)
        if log:
            log(msg)

    system = platform.system()
    emit("🔧 One-click setup: applying checklist items for this machine...")

    if system == "Windows":
        results = _optimize_windows()
    elif system == "Darwin":
        results = _optimize_macos()
    else:
        emit(f"⚠️ Unsupported OS '{system}' - please set everything manually.")
        return {}

    icons = {"ok": "✅", "skip": "⏭️", "warn": "⚠️"}
    for status, message in results.values():
        emit(f"{icons.get(status, '•')} {message}")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    optimize_system()
