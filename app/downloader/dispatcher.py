# -*- coding:utf-8 -*-
import os
import traceback
from app.downloader.tools import utils as tools
from app.downloader import config, api
from app.downloader.tools import WebDownloader
from app.schemas.tasks import DispatchedTask


class TaskDispatcher:
    
    def __init__(self):
        self.saveTempFile = config.saveTempFile
        self.hlsThreadCnt = config.hlsThreadCnt
        self.fragThreadCnt = config.fragThreadCnt
        self.fragmentCnt = config.fragmentCnt
        self.correctTimestamp = config.correctTimestamp
        self.tempFilePath = tools.realPath(config.tempFilePath)
        self.videoFilePath = tools.realPath(config.videoFilePath)

        self.task = None

        tools.mkdirIfNotExists(self.tempFilePath)
        tools.mkdirIfNotExists(self.videoFilePath)
        tools.checkFFmpeg()
        tools.setupRequestLogger(config.logPath)
        tools.setupDebug(config.debug)


    # hls: 下载所有ts分片并合并
    def _downloadHls(self, urls, fileName, downloader, headers = {}, correct = False):
        print("-- dispatcher/downloadHls")

        tempFileBase = tools.join(self.tempFilePath, fileName)
        fileNames = tools.generateFileNames(urls, tempFileBase)
        targetFileName = tools.join(self.videoFilePath, fileName + '.mp4')

        downloader.downloadAll(urls, fileNames, headers, self.hlsThreadCnt)
        tools.mergePartialVideos(fileNames, targetFileName, correct=correct)

        self.saveTempFile or tools.removeFiles(fileNames)
        return targetFileName

    # dash: 下载音频和视频并合并
    def _downloadDash(self, audioUrls, videoUrls, fileName, downloader, headers = {}):
        print("-- dispatcher/downloadDash")

        tempAudioBase = tools.join(self.tempFilePath, fileName + '.audio')
        tempVideoBase = tools.join(self.tempFilePath, fileName + '.video')
        audioNames = tools.generateFileNames(audioUrls, tempAudioBase)
        videoNames = tools.generateFileNames(videoUrls, tempVideoBase)
        targetFileName = tools.join(self.videoFilePath, fileName + '.mp4')

        downloader.multiThreadDownloadAll(audioUrls, audioNames, headers, \
            self.fragThreadCnt, self.fragmentCnt)
        downloader.multiThreadDownloadAll(videoUrls, videoNames, headers, \
            self.fragThreadCnt, self.fragmentCnt)
        tools.mergeAudio2Video(audioNames, videoNames, targetFileName)

        self.saveTempFile or tools.removeFiles(audioNames + videoNames)
        return targetFileName

    # 普通分段视频: 下载并合并
    def _downloadPartialVideos(self, urls, fileName, downloader, headers = {}):
        print("-- dispatcher/downloadPartialVideos")

        tempFileBase = tools.join(self.tempFilePath, fileName)
        fileNames = tools.generateFileNames(urls, tempFileBase)
        suffix = tools.getSuffix(urls[0])
        targetFileName = tools.join(self.videoFilePath, fileName + suffix)

        for i, url in enumerate(urls):
            downloader.multiThreadDownload(url, fileNames[i], headers, \
                self.fragThreadCnt, self.fragmentCnt)
        tools.mergePartialVideos(fileNames, targetFileName)

        self.saveTempFile or tools.removeFiles(fileNames)
        return targetFileName

    # websocket视频流，保存至本地并合并
    def handleStream(self, extendInfo:DispatchedTask, fileName, audioFormat, videoFormat, **desc):
        print("-- dispatcher/handleStream")

        audioName = tools.join(self.tempFilePath, fileName + '.audio' + audioFormat)
        videoName = tools.join(self.tempFilePath, fileName + '.video' + videoFormat)
        targetFileName = tools.join(self.videoFilePath, fileName + '.mp4')
        downloader = WebDownloader(saveTempFile=self.saveTempFile, extendInfo=extendInfo, fileName=fileName)
        downloader.saveStream(audioName, videoName, **desc)
        tools.mergeAudio2Video([audioName], [videoName], targetFileName)

        self.saveTempFile or tools.removeFiles([audioName, videoName])
        print('Finish %s\n' % targetFileName)
        return targetFileName

    # 下载弹幕并集成到视频文件
    def handleSubtitles(self, subtitles, fileName, videoName, downloader, headers = {}):
        subtitleUrls, subtitleNames = [], []
        subtitlesInfo = []

        for name, url in subtitles:
            subtitleUrls.append(url)
            subtitleName = tools.join(self.tempFilePath, '%s_%s%s' % \
                (fileName, name, tools.getSuffix(url)))
            subtitleNames.append(subtitleName)
            subtitlesInfo.append((name, subtitleName))

        downloader.downloadAll(subtitleUrls, subtitleNames, headers, self.hlsThreadCnt)

        for each in subtitleNames:
            tools.tryFixSrtFile(each)
        
        targetFileName = tools.integrateSubtitles(subtitlesInfo, videoName)
        self.saveTempFile or tools.removeFiles(subtitleNames)
        return targetFileName


    def download(self, url, fileName, extendInfo:DispatchedTask, data = None):
        fileName = tools.escapeFileName(fileName)
        videoType, headers, audioUrls, videoUrls, subtitles = api.parseSingleUrl(url, data)

        if audioUrls:
            print('匹配到%d段音频，%d段视频，开始下载' % (len(audioUrls), len(videoUrls)))
        else:
            print('匹配到%d段视频，开始下载' % len(videoUrls))

        targetFileName = ''
        downloader = WebDownloader(saveTempFile=self.saveTempFile, extendInfo=extendInfo, fileName=fileName)

        if videoType == 'hls':
            # 存在字幕文件时，使用二进制合并以校正时间戳
            correct = self.correctTimestamp or bool(subtitles)
            targetFileName = self._downloadHls(videoUrls, fileName, downloader, headers, correct)
        elif videoType == 'dash':
            targetFileName = self._downloadDash(audioUrls, videoUrls, fileName, downloader, headers)
        elif videoType == 'partial':
            targetFileName = self._downloadPartialVideos(videoUrls, fileName, downloader, headers)

        if subtitles:
            print('匹配到%d个字幕，开始下载' % len(subtitles))
            targetFileName = self.handleSubtitles(subtitles, fileName, targetFileName, downloader, headers)

        print('Finish: %s\n' % targetFileName)


    def downloadMultiParts(self, url, baseFileName, pRange, extendInfo:DispatchedTask):
        startP, endP, allPartInfo = api.parseMultiPartUrl(url, pRange)

        print('准备下载第%d-%dP\n' % (startP, endP))

        for i in range(startP-1, endP):
            p = i + 1
            partName, videoUrl = allPartInfo[i]['name'], allPartInfo[i]['videoUrl']
            fileName = 'P%03d__%s__%s' % (p, baseFileName, partName)
            print('开始下载第%dP: %s' % (p, fileName))
            self.download(videoUrl, fileName, DispatchedTask(extendInfo.id, f'{p}', isSubTask=True))

    def dispatch(self, **task):
        self.task = task
        task['type'] = task.get('type', 'link')
        print()

        try:
            enxtendInfo = DispatchedTask(task.get('id'), task.get('pRange'))
            if task['type'] == 'link':
                url, fileName = task.get('linksurl') or task['url'], task['fileName']
                data = task.get('data')
                if task.get('pRange'):
                    self.downloadMultiParts(url, fileName, task['pRange'], enxtendInfo)
                else:
                    self.download(url, fileName, enxtendInfo, data)
            elif task['type'] == 'stream':
                self.handleStream(enxtendInfo, *task)
        except Exception as e:
            print('-' * 100)
            traceback.print_exc()
            print('-' * 100)
        except KeyboardInterrupt:
            self.shutdown()
        finally:
            task['type'] == 'stream' and task['close']()
            self.task = None

    def shutdown(self):
        if self.task:
            task = self.task
            self.task = None

            if task['type'] == 'stream':
                task['dataQueue'].put(KeyboardInterrupt())
            # self.downloader.shutdownAndClean()