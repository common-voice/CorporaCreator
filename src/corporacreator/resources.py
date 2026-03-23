"""Resource monitoring utilities for CorporaCreator.

Provides memory and resource logging at critical pipeline points.
Used with -vv (DEBUG) to diagnose OOM kills in containerized environments.

Platform support:
  - Linux/container: reads /proc/self/status (VmRSS, VmSize, VmPeak)
  - macOS: resource.getrusage fallback (ru_maxrss in bytes)
  - Windows: psutil if available, otherwise gracefully skipped
"""

import logging
import sys

_logger = logging.getLogger(__name__)


def get_memory_mb() -> dict:
    """Returns memory usage in MB from available sources.

    Tries platform-specific methods in order of accuracy.
    Note: some fallbacks (e.g. resource.getrusage) report peak RSS, not current.
    Never raises -- returns empty dict on failure so callers are safe.
    """
    result: dict = {}

    # 1. Linux /proc/self/status -- most accurate for containers
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    result["rss"] = int(line.split()[1]) / 1024  # kB -> MB
                elif line.startswith("VmSize:"):
                    result["vm"] = int(line.split()[1]) / 1024
                elif line.startswith("VmPeak:"):
                    result["peak"] = int(line.split()[1]) / 1024
        if result:
            return result
    except (FileNotFoundError, PermissionError, OSError):
        pass

    # 2. Unix fallback (macOS, Linux without /proc)
    if sys.platform != "win32":
        try:
            import resource
            ru = resource.getrusage(resource.RUSAGE_SELF)
            # ru_maxrss: KB on Linux, bytes on macOS
            divisor = 1024 * 1024 if sys.platform == "darwin" else 1024
            result["rss_max"] = ru.ru_maxrss / divisor
            return result
        except (ImportError, OSError):
            pass

    # 3. Windows fallback -- psutil (optional dependency)
    try:
        import psutil  # type: ignore
        proc = psutil.Process()
        mem = proc.memory_info()
        result["rss"] = mem.rss / (1024 * 1024)
        result["vm"] = mem.vms / (1024 * 1024)
        if hasattr(mem, "peak_wset"):
            result["peak"] = mem.peak_wset / (1024 * 1024)  # type: ignore
        return result
    except Exception:
        pass

    return result


def format_memory(mem: dict) -> str:
    """Formats memory dict as a compact string for log output."""
    parts = []
    for key in ("rss", "vm", "peak", "rss_max"):
        if key in mem:
            parts.append(f"{key}={mem[key]:.0f}MB")
    return " ".join(parts) if parts else "unavailable"


def log_resources(label: str, extra: str = "") -> None:
    """Logs current memory usage at DEBUG level with a descriptive label.

    Args:
        label: Short description of the pipeline point (e.g. "after read_csv").
        extra: Optional extra info to append (e.g. row counts, DataFrame size).
    """
    if not _logger.isEnabledFor(logging.DEBUG):
        return
    mem = format_memory(get_memory_mb())
    suffix = f" | {extra}" if extra else ""
    _logger.debug("[RESOURCES] %s: %s%s", label, mem, suffix)
