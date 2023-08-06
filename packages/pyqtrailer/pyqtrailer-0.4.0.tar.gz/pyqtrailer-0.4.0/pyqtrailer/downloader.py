
from multiprocessing import Process, Queue, active_children
import subprocess
import os
import signal
import locale
import errno

class ClosingException(Exception):
    pass


class DownloadStatus:
    DONE = 1
    ERROR = 2
    IN_PROGRESS = 3
    WAITING = 4

    def __init__(self, url, status, percent=0):
        self.status = status
        self.url = url
        self.percent= percent



class TrailerDownloader(object):

    def __init__(self, taskQueue, taskDict, parallelProcesses = 1):
        """taskQueue = Queue() of (url, targetDir) to download
        taskDict = dictonary with url as key and DownloadStatus as value
        parallelProcesses = number of processes downloading in parallel
        """

        self.taskQueue = taskQueue
        self.taskDict = taskDict
        self.parallelProcesses = parallelProcesses
        self.processes = []

        self._downloadFunc = trailerDownload


    def start(self):
        for i in range(self.parallelProcesses):
            p = Process(target=trailerDownload,
                        args=(self.taskQueue,
                              self.taskDict))
            p.start()
            self.processes.append(p)

    def stop(self):
        for p in self.processes:
            p.terminate()




def trailerDownload(taskQueue, taskDict):
    # we need to have consistent wget output
    locale.setlocale(locale.LC_ALL, "C")
    signal.signal(signal.SIGTERM, term_handler)
    try:
        while True:
            trailerURL, targetDir = taskQueue.get()
            command = ['wget','-cN',
                       '-U',
                       'QuickTime/7.6.2 (qtver=7.6.2;os=Windows NT 5.1Service Pack 3)',
                       trailerURL,
                       '-P',
                       targetDir,
                       '--progress=dot:mega']
            downloadFunc(trailerURL, command, taskDict)
    except ClosingException as e:
        pass

wgetPids=[]
def downloadFunc(trailerURL, command, taskDict):
    print("Executing: %s" % " ".join(command))
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    taskDict[trailerURL] = DownloadStatus(trailerURL,
                                          DownloadStatus.IN_PROGRESS)
    wgetPids.append(p.pid)
    totalsize = 0
    while True:
        line = p.stderr.readline().decode()
        if len(line) == 0:
            break
        if line.find('Length:') != -1:
            totalsize = int(line.split(' ')[1])
            break

    # now we start counting dots :-)
    downloaded = 0
    while True:
        x = p.stderr.read(1).decode()

        if len(x) == 0:
            break
        if x == '.' or x ==',':
            downloaded = downloaded + 64 * 1024
        perc = int(downloaded * 100 / totalsize)
        if perc % 5 == 0:
            try:
                taskDict[trailerURL] = DownloadStatus(trailerURL,
                           DownloadStatus.IN_PROGRESS,
                           perc)
            except IOError as e:
                print("Ignoring interrupted assignement exception")
                if e.errno is not errno.EINTR:
                    raise

    p.wait()
    if p.returncode is not 0:
        taskDict[trailerURL] = DownloadStatus(trailerURL,
                           DownloadStatus.ERROR)
    else:
        taskDict[trailerURL] = DownloadStatus(trailerURL,
                           DownloadStatus.DONE)
    wgetPids.remove(p.pid)


def term_handler(signum, frame):
    for p in wgetPids:
        print('Stopping wget process ', p)
        os.kill(p, signal.SIGTERM)
    raise ClosingException("Finishing up")
