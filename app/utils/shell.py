# -*- coding:utf-8 -*-

import subprocess,time
from threading import Thread
from app.utils import func_handler

class Bashshell():
    def __init__(self,update,context):
        self.update = update
        self.context = context
        self.args = ' '.join(context.args[:])
        self.chat_id = update.message.chat_id
        message = context.bot.send_message(chat_id=self.chat_id, text="bash start ...")
        self.message_id = message.message_id
        

    def task_buffer(self):
        func_handler.Task.Msg[self.message_id]=0
        self.progress = Thread(target=self.task_process)
        self.progress.daemon = True
        self.progress.start()
       

    def task_process(self):
        tou = ''
        for output in self.run(self.args):
            if func_handler.Task.Msg[self.message_id]==1:
                self.shellprocess.kill()
                break
            if output:
                tou = tou +'\n' +output
                if len(tou) > 2000:
                    tou = tou[100:] 
                self.context.bot.edit_message_text(chat_id=self.chat_id, message_id= self.message_id, text=str(tou),  disable_web_page_preview=True)
                time.sleep(1)
        tou = tou +'\n' + '         --------Shell Stopped--------'
        self.context.bot.edit_message_text(chat_id=self.chat_id, message_id= self.message_id, text=str(tou),  disable_web_page_preview=True)


    def run(self,command):
        self.shellprocess = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            errors="ignore",
            universal_newlines=True,
        )
        for line in iter(self.shellprocess.stdout.readline, 'b'):
            #line = self.shellprocess.stdout.read().strip()
            if not line:
                break
            yield line.strip()
        
        self.shellprocess.communicate()

if __name__ == '__main__':
    ll = Bashshell()
    ll.task_process('dir')
