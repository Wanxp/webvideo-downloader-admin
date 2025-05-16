# -*- coding:utf-8 -*-
import json
import threading
import queue
from app.downloader.dispatcher import TaskDispatcher
from app.downloader.tools import utils as tools
from app.downloader import config


# 守护模式下的后台队列
class DownloadQueue:
    ESTABLISHED = 0
    IN_TRANSIT = 1
    DATA_CACHE_SIZE = 10

    # 等待下载的任务队列
    taskQueue = queue.Queue()

    def put(self, task):
        task=task.to_dict()
        task['pRange']=task['pRange'].replace('-', ' ') if task['pRange'] else None
        self.taskQueue.put(task)

    def new_client(self, client):
        client.status = self.ESTABLISHED

    def printWithoutData(self, task):
        copyTask = {key: task[key] for key in task}
        if copyTask.get('data'):
            copyTask['data'] = '...'
        print('\nReceive: %s\n' % tools.stringify(copyTask))


class Runner:
    def __init__(self):
        self.taskDispatcher = TaskDispatcher()

    def start(self):
        if config.interactive:
            self.startInteractive()
        else:
            self.startDaemon(config.port)

    # 交互模式，接受用户输入
    def startInteractive(self):
        while True:
            try:
                url = input('输入暴力猴链接或本地m3u8路径: ').strip()
                fileName = input('输入文件名: ').strip()
                isMultiPart = url.find('www.bilibili.com') != -1
                pRange = input('输入首、尾P(空格分隔)或单P: ').strip() if isMultiPart else None
            except KeyboardInterrupt:
                break

            self.taskDispatcher.dispatch(url=url, fileName=fileName, pRange=pRange)

    # 守护模式，监听web请求
    def startDaemon(self, port):
        # 消费者
        t = threading.Thread(target=self._downloadThread, daemon=True)
        t.start()

    def _downloadThread(self):
        while True:
            task = DownloadQueue.taskQueue.get()
            print('Handle: "%s"' % task['fileName'])
            self.taskDispatcher.dispatch(**task)



if __name__ == '__main__':
    runner = Runner()
    runner.start()
