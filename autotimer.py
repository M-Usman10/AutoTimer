import asyncio
import logging
import time

import uiautomation as auto
import win32gui

from db import Data
from tools import url_to_name,get_date
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
                logging.info(active_window_name)
                total_activity_duration = time.time() - start_time
                async with asyncio.Lock():
                    self.time_logs[get_date()][active_window_name]["duration"] += total_activity_duration
                active_window_name = activity
            await asyncio.sleep(5)

    async def save_logs(self):
        await asyncio.sleep(DATA_SYNC_DURATION)
        async with asyncio.Lock():
            logging.info("Saving Data to Json")
            self.data.save_time_logs(self.time_logs)

async def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt = "%d:%m:%Y--%H:%M:%S")
    tracker = TimeTracker()
    track_time = asyncio.create_task(tracker.track_time())
    save_logs = asyncio.create_task(tracker.save_logs())
    await save_logs
    await track_time

if __name__ == "__main__":
    asyncio.run(main())