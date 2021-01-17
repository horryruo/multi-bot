import sys, os
from git import Repo
import time
from datetime import datetime, timedelta
from function_requests import get_html

class Version(object):
    def __init__(self, repo_url, branch='master'):
        self.local_path = os.getcwd()
        self.repo_url = repo_url
        self.repo = None
        self.repo = Repo(self.local_path)
        self.remote = self.repo.remote()

    def get_time(self,log='false'):
        html = get_html('https://api.github.com/repos/horryruo/multi-bot','json')
        updatetime = html.get('pushed_at')
        #转换成时间数组
        timeArray = time.strptime(updatetime,"%Y-%m-%dT%H:%M:%SZ")
        #转换成时间戳
        timestamp = time.mktime(timeArray)
        #转换成datetime
        c_time = datetime.fromtimestamp(timestamp)
        #+8时区
        dt = c_time + timedelta(hours=8)
        #换回+8时间格式
        #timeArray_8 = time.strptime(str(dt),"%Y-%m-%d %H:%M:%S")
        #timestamp_8 = time.mktime(timeArray_8)
        if log =='true':
            commit_all = self.commits()
            commitlastest = commit_all[0].get('date')
            return dt,commitlastest
        '''
        if timestamp_8 and commitlastest:
            commit_stamp = time.mktime(time.strptime(commitlastest, '%Y-%m-%d %H:%M'))
            
            if int(commit_stamp) > int(timestamp_8):
                uptime=1
            else:
                uptime=2
                '''
        return dt
        '''
    def git_repo(self):
        repo = Repo(self.dir)#config="http.proxy='http://127.0.0.1:7890'")
        
        remote = repo.remote()
        print(remote.pull())
        #g = Git(self.dir)
        #g.pull('origin','master')
        '''
    

    def initial(self, repo_url, branch):
        '''
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(repo_url, to_path=self.local_path, branch=branch)
        else:
            
        self.repo = Repo(self.local_path)
        '''
        pass

    def pull(self,mode='git'):
        """
        从线上拉最新代码
        :return:
        """
        if mode=='repo':
            return self.remote.pull()
        elif mode=='git':
            return self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
                                       max_count=50,
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def change_to_branch(self, branch):
        """
        切换分值
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, branch, commit):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset('--hard', commit)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)
        



if __name__ == "__main__":
    repo = Version('https://github.com/horryruo/multi-bot.git')
    print(repo.pull())
    
    