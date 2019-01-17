"""Script to start the release monitor."""

from release_monitor.release_monitor import ReleaseMonitor

if __name__ == '__main__':
    monitor = ReleaseMonitor()
    monitor.run()
