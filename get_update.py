import sys, os
from git import Repo,Git
import time
from datetime import datetime, timedelta
from function_requests import get_html

class Version(object):
    def __init__(self):
        self.dir = os.getcwd()

    def get_time(self):
        html = get_html('https://api.github.com/repos/horryruo/multi-bot','json')
        updatetime = html.get('pushed_at')
        #转换成时间数组
        timeArray = time.strptime(updatetime,"%Y-%m-%dT%H:%M:%SZ")
        #dt = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
        timestamp = time.mktime(timeArray)
        c_time = datetime.fromtimestamp(timestamp)
        dt = c_time + timedelta(hours=8)
        return dt
    def git_repo(self):
        repo = git.Repo(self.dir,config="http.proxy='http://127.0.0.1:7890'")
        remote = repo.remotes.origin
        remote.pull()
        #g = Git(self.dir)
        #g.pull('origin','master')
        
        



if __name__ == "__main__":
    Version.git_repo
    