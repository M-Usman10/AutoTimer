import asyncio
import time

import uiautomation as auto
import win32gui

from db import Data
from tools import url_to_name
from configs import DATA_SYNC_DURATION

class TimeTracker:
    """
    Time tracker records time of ongiong screen activities, save time logs to local storage and sync them with MongoDB
    """
    def __init__(self):
        self.data = Data(db_name="time-logs",collection_name="logs-data")
        self.data.make_collection()

    @staticmethod
    def get_active_window():
        """
        Returns the name of currently running foreground window
        """
        _active_window_name = None
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
        return _active_window_name


    @staticmethod
    def get_chrome_url():
        """
        Returns the url opened in chromw
        """
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value

    async def track_time(self):
        """
        Tracks activities and saves info to cloud db and to local storage as json
        """

        self.time_logs = self.data.load_time_logs()
        start_time = time.time()
        active_window_name=""
        while True:
            activity = self.get_active_window()
            if 'Google Chrome' in activity:
                activity = url_to_name(self.get_chrome_url())
            if active_window_name != activity:
                print(active_window_name)
                total_activity_duration = time.time() - start_time
                async with asyncio.Lock():
                    self.time_logs[active_window_name]["duration"] += total_activity_duration
                active_window_name = activity
            time.sleep(1)

    async def save_logs(self):
        await asyncio.sleep(DATA_SYNC_DURATION)
        async with asyncio.Lock():
            self.data.save_time_logs()

if __name__ == "__main__":
    tracker = TimeTracker()
    await asyncio.create_task(tracker.track_time())
    await asyncio.create_task(tracker.save_logs())