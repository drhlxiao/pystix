#!/usr/bin/python3
# @author       : Hualin Xiao
# @date         : Mar. 06, 2023
# @description:  manage a task


import time
import threading
from stix.core import logger
logger = logger.get_logger()


class TaskManager(object):
    def __init__(self, task_name=''):
        self.sleep_time=120
        self.max_exec_time = 3600
        self.task_name=task_name
    def check_running_thread(self,thread):
        # Define a function to check if the thread is running for more than 2 hours
        if not thread.is_alive():
            logger.info(f"Task {self.task_name} not running, restarting...")
            self.run()
            return
        else:
            if time.time() - thread.start_time > self.max_exec_time:  
                logger.warning(f"Task {self.task_name} has been running for more than {self.max_exec_time} sec, restarting...")
                thread.kill()
                self.run()

    def run(self, func,  sleep_time=120, max_exec_time=7200  ):
        # Define a function to start the thread
        """
        sleep time: excuation time
        """
        self.sleep_time = sleep_time
        self.max_exec_time = max_exec_time
        logger.info(f'starting task {self.task_name}...')
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start_time = time.time()
        thread.kill = lambda: None
        thread.start()

        # Check the thread every 5 minutes
        while True:
            time.sleep(self.sleep_time) # 5 minutes in seconds
            self.check_running_thread(thread)


