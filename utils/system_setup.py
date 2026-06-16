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
import re
import subprocess


def _run(cmd):
    """Run a command, raising on non-zero exit. Output is captured/silenced."""
    subprocess.run(cmd, capture_output=True, check=True)


# ANSI color codes for the status tags.
_RESET = "\033[0m"
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"

# Map an action status to a fixed-width, color-coded tag.
_TAGS = {
    "ok": f"{_GREEN}[ OK ]{_RESET}",
    "skip": f"{_YELLOW}[SKIP]{_RESET}",
    "warn": f"{_RED}[FAIL]{_RESET}",
}


def _enable_ansi():
    """Enable ANSI escape sequences on Windows consoles (no-op elsewhere)."""
    if platform.system() != "Windows":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        # STD_OUTPUT_HANDLE = -11, ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


# Short title shown before each action's message (mirrors the README checklist).
TITLES = {
    "power_mode": "Check power mode",
    "brightness": "Check screen brightness",
    "screen_off": "Check screen timeout",
    "network": "Check network",
    "bluetooth": "Check Bluetooth",
    "battery_saver": "Check battery saver",
    "low_batt_brightness": "Check low-battery dimming",
    "volume": "Check volume",
}


def _check_network():
    """Read-only: confirm we can reach the internet (we can't auto-join Wi-Fi)."""
    import socket

    try:
        socket.setdefaulttimeout(3)
        socket.create_connection(("8.8.8.8", 53)).close()
        return ("ok", "Internet connection is active")
    except Exception:
        return ("warn", "No internet detected - connect to Wi-Fi before testing")


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


def _macos_bluetooth():
    """Report Bluetooth state; enable it with blueutil if that tool is present.

    Reads the controller state from `system_profiler` (the per-host plist key
    `ControllerPowerState` is gone on recent macOS). The first "State:" line in
    SPBluetoothDataType is the controller's power state.
    """
    import shutil

    state = ""
    try:
        out = subprocess.run(
            ["system_profiler", "SPBluetoothDataType"],
            capture_output=True, text=True, check=True,
        ).stdout
        for line in out.splitlines():
            stripped = line.strip()
            if stripped.startswith("State:"):
                state = stripped.split(":", 1)[1].strip().lower()
                break
    except Exception:
        state = ""

    if state == "on":
        return ("ok", "Bluetooth is already on")

    if shutil.which("blueutil"):
        try:
            _run(["blueutil", "--power", "1"])
            return ("ok", "Turned Bluetooth on (blueutil)")
        except Exception as e:
            return ("warn", f"Could not enable Bluetooth: {e}")

    if state == "off":
        return ("warn", "Bluetooth is off - turn it on manually (or install blueutil)")
    return ("skip", "Could not read Bluetooth state - verify manually")


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

    # 4. Network (read-only) and Bluetooth.
    results["network"] = _check_network()
    results["bluetooth"] = _macos_bluetooth()

    # 5. Battery saver @ 30% - not configurable on macOS.
    results["battery_saver"] = ("skip", "Low Power threshold is not configurable on macOS")

    # 6. Lower brightness on low battery - not scriptable on macOS.
    results["low_batt_brightness"] = ("skip", "Not scriptable on macOS - verify manually")

    # 7. Volume 0%
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


def _windows_bluetooth():
    """Check Bluetooth via the WinRT Radio API and turn it on if it's off."""
    ps_code = """
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
    Function Await($WinRtTask, $ResultType) {
        $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
        $netTask = $asTask.Invoke($null, @($WinRtTask))
        $netTask.Wait(-1) | Out-Null
        $netTask.Result
    }
    [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
    $radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])
    $bluetooth = $radios | Where-Object { $_.Kind -eq 'Bluetooth' }
    if ($bluetooth) {
        if ($bluetooth.State -eq 'Off') {
            Await ($bluetooth.SetStateAsync('On')) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
            Write-Output "Enabled"
        } else {
            Write-Output "AlreadyOn"
        }
    } else {
        Write-Output "NotFound"
    }
    """
    try:
        out = subprocess.run(
            ["powershell", "-Command", ps_code], capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception as e:
        return ("warn", f"Could not check/enable Bluetooth: {e}")

    if "Enabled" in out:
        return ("ok", "Bluetooth was off, turned it on")
    if "AlreadyOn" in out:
        return ("ok", "Bluetooth is already on")
    if "NotFound" in out:
        return ("warn", "No Bluetooth adapter detected")
    return ("warn", f"Bluetooth status: {out}")


# PowerShell that mutes the default playback device via the Core Audio
# IAudioEndpointVolume COM interface. The interface methods must be declared in
# vtable order so SetMute lands on the right slot; the ones we don't call still
# need to occupy their positions. Unlike SendKeys([char]173) this needs no
# window focus and *sets* the mute state (rather than toggling it), so it works
# reliably and never accidentally unmutes an already-muted machine.
_WIN_MUTE_PS = r'''
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
  int RegisterControlChangeNotify(System.IntPtr n);
  int UnregisterControlChangeNotify(System.IntPtr n);
  int GetChannelCount(out int c);
  int SetMasterVolumeLevel(float a, System.Guid b);
  int SetMasterVolumeLevelScalar(float a, System.Guid b);
  int GetMasterVolumeLevel(out float a);
  int GetMasterVolumeLevelScalar(out float a);
  int SetChannelVolumeLevel(uint ch, float a, System.Guid b);
  int SetChannelVolumeLevelScalar(uint ch, float a, System.Guid b);
  int GetChannelVolumeLevel(uint ch, out float a);
  int GetChannelVolumeLevelScalar(uint ch, out float a);
  int SetMute([MarshalAs(UnmanagedType.Bool)] bool m, System.Guid b);
  int GetMute(out bool m);
}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice { int Activate(ref System.Guid id, int clsCtx, System.IntPtr act, [MarshalAs(UnmanagedType.IUnknown)] out object o); }
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator { int NotImpl(); int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice ep); }
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject { }
public class Audio {
  public static void Mute() {
    var e = (IMMDeviceEnumerator)(new MMDeviceEnumeratorComObject());
    IMMDevice dev; e.GetDefaultAudioEndpoint(0, 1, out dev);
    System.Guid g = typeof(IAudioEndpointVolume).GUID;
    object o; dev.Activate(ref g, 23, System.IntPtr.Zero, out o);
    ((IAudioEndpointVolume)o).SetMute(true, System.Guid.Empty);
  }
}
'@
[Audio]::Mute()
'''


def _optimize_windows():
    results = {}

    # 1. Power mode -> Balanced.
    #    On modern Windows 11 the visible "Power mode" is an *overlay* (Best
    #    power efficiency / Balanced / Best performance) layered on top of the
    #    power *scheme*. `powercfg /setactive` only changes the scheme, so on a
    #    machine that already has the Balanced scheme it does nothing visible and
    #    the slider can stay stuck on "Best performance". Set both: the Balanced
    #    scheme (covers classic / OEM custom plans) and the Balanced overlay.
    try:
        _run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"])
        # The all-zero overlay GUID is the Balanced position of the Power mode
        # slider. Unsupported on older Windows (no overlays) where the scheme is
        # the power mode, so don't let it fail the whole step.
        try:
            _run(["powercfg", "/overlaysetactive", "00000000-0000-0000-0000-000000000000"])
        except Exception:
            pass
        results["power_mode"] = ("ok", "Set power plan and power mode to Balanced")
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

    # 4. Network (read-only) and Bluetooth.
    results["network"] = _check_network()
    results["bluetooth"] = _windows_bluetooth()

    # 5. Battery saver @ 30%.
    try:
        _run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_ENERGYSAVER", "ESBATTTHRESHOLD", "30"])
        _run(["powercfg", "/setactive", "SCHEME_CURRENT"])
        results["battery_saver"] = ("ok", "Set Battery Saver to turn on at 30%")
    except Exception as e:
        results["battery_saver"] = ("warn", f"Could not set Battery Saver threshold: {e}")

    # 6. Turn "lower brightness on low battery" off (no dimming -> 100%).
    try:
        _run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_ENERGYSAVER", "ESBRIGHTNESS", "100"])
        _run(["powercfg", "/setactive", "SCHEME_CURRENT"])
        results["low_batt_brightness"] = ("ok", "Disabled 'lower brightness on low battery'")
    except Exception as e:
        results["low_batt_brightness"] = ("warn", f"Could not disable low-battery dimming: {e}")

    # 7. Volume 0% - mute the default playback device via Core Audio.
    try:
        _run(["powershell", "-Command", _WIN_MUTE_PS])
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
        # Log file and GUI callback get a plain version (no ANSI color codes).
        plain = re.sub(r"\033\[[0-9;]*m", "", msg)
        logging.info(plain)
        if log:
            log(plain)

    _enable_ansi()

    system = platform.system()
    print()  # blank line before the checklist for readability
    emit("One-click setup: applying checklist items for this machine...")

    if system == "Windows":
        results = _optimize_windows()
    elif system == "Darwin":
        results = _optimize_macos()
    else:
        emit(f"{_TAGS['warn']} Unsupported OS '{system}' - please set everything manually.")
        print()
        return {}

    for key, (status, message) in results.items():
        tag = _TAGS.get(status, f"[{status.upper()}]")
        title = TITLES.get(key, key)
        emit(f"{tag} {title}: {message}")

    print()  # blank line after the checklist for readability
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
    optimize_system()
