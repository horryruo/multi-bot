# -*- coding: utf-8 -*-
import telegram 
import os
import sys
from threading import Thread
import logging
from functools import wraps
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from monthly import monthly_thread
from jav_thread import thread_javlib
from magnet import sukebei
from dmm import dmm_thread, prevideo, prephotos, dmmonecid, prevideolow, dmmsearch, dmmlinks
from cloudflare import CloudFlare_handler
from loadini import read_config
import time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




ifproxy,proxy,token,users = read_config()
TOKEN = token
userid = users.split(',')
userss = []
#userid = ','.join(userid)
for i in userid:
    userss.append(int(i))
#print(userid)
#userids = ','.join(userss)
LIST_OF_ADMINS = userss
REQUEST_KWARGS={
        # "USERNAME:PASSWORD@" is optional, if you need authentication:
    'proxy_url': 'http://%s/'%proxy,
}   





def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    #update.message.reply_text(str(update.message.text))
    update.message.reply_text(str(context.error))

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            error = "Unauthorized access denied for you!!you user id:{}.".format(user_id)
            update.message.reply_markdown(error)
            print(error)
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def long_message(update, context, text: str):
    max_length = telegram.constants.MAX_MESSAGE_LENGTH
    if len(text) <= max_length:
        
        return update.message.reply_markdown(text)

    parts = []
    while len(text) > max_length:
        parts.append(text[:max_length])
        text = text[max_length:]
    parts.append(text)
    msg = None
    for part in parts:
        update.message.reply_text(part)
        time.sleep(3)
    return msg



        
    

@send_typing_action
def start(update, context):
    text = '''
    ******
    欢迎使用imulti bot，请输入/help查看指令
    ******
    '''
    #print(telegram.constants.MAX_MESSAGE_LENGTH)
    update.message.reply_markdown(text)

@send_typing_action
def help(update, context):
    text = '''
    *all command for bot*
    *start* - `欢迎  `
    *help* - `帮助`
    *m* - `查询是否ikoa月额，num/cid皆可   /m ssni-520`
    *uid* - `查询女优在dmm所有番号，需女优id  /uid 2333`
    *lib* - `查询女优在library所有番号，需女优页面链接  /lib https://*****`
    *video* - `dmm预览视频，需准确cid，且不完善`
    *photo* - `dmm预览图片，需准确cid`
    *cid* -  `查询番号具体信息，支持cid/num `
    *magnet* -  `搜索关键词在sukebei`
    *search* -  `搜索关键词在dmm，dmm官方支持正则`
    *links* -  `demo for links in dmm limit 30 project`
    *new* -  `dmm new video limit 30`
    *top* -  `dmm hot video limit 30`
    *cf* -  `operation cloudflare dns only admin`
    *restart* - `only admin useful `

    *cf help* ==>  `ls` => lsallzome    example: /cf ls
                   `dns domain` => *load dns for domain*   example:  /cf dns domain
                   `add type domain host ` => *add dns records for domain*   example: /cf add A test.domain.com ip-adress
                   `edit type domain host (option:cloudon/off ,ttl = ini)` => *edit dns records for domain*   example:/cf edit A test.domain.com ip-adress cloudon
                   `del domain` => *delete dns for domain*  example: /cf del test.domain.com
    '''
    update.message.reply_markdown(text)



@restricted
@send_typing_action 
def monthlyy(update, context):
    #print(context.args)
    chat_id=update.message.chat_id
    id = context.args
    #print(id)
    idlist = ','.join(id)
    searchlist1 = idlist.split(',')
    leng3 = len(searchlist1)
    update.message.reply_text('正在查询%s个...请稍候......' %leng3)
    
    mon,leng,nomon,leng1,time,tbb,tbbb = monthly_thread(idlist)
    tb = str(tbb)
    usetime = '耗时:' + time + '秒'
    if leng == 0:
        if leng1 == 0:
            result = '无结果'
            update.message.reply_text(result)
        else:
            result1 = '非月额list (%s) => %s' %(leng1,nomon)
            update.message.reply_text(tb)
            update.message.reply_text(result1)
            update.message.reply_text(usetime)
    else:
        if leng1 == 0:
            update.message.reply_text(tb)
            result = '月额list (%s) => %s' %(leng,mon)
            update.message.reply_text(result)
            update.message.reply_text(usetime)
        else:
            result = '月额list (%s) => %s' %(leng,mon)
            result1 = '非月额list (%s) => %s' %(leng1,nomon)
            update.message.reply_text(tb)
            update.message.reply_text(result)
            update.message.reply_text(result1)
            update.message.reply_text(usetime)
    
@restricted
@send_typing_action  
 
def dmmid(update, context):
    searchid = context.args[0]
    update.message.reply_text('search items for %s please wait...'%searchid)
    
    result,time = dmm_thread(searchid)
    usetime = '搜索完成，耗时:' + time + '秒'
    update.message.reply_text(usetime)
    #update.message.reply_text(result)
    if len(result) > 4096:
        mssg = '超出telegram消息限制，将分段截取，取最后10字符用于校验：' + result[-10:]
        update.message.reply_text(mssg)
    msg = long_message(update,context,result)

    
@restricted
@send_typing_action
def dmmcid(update,context):
    searchid = context.args[0]
    if len(context.args) == 1:
        searchidd = context.args[0]
        searchidd = searchidd.replace('-',' ')
    else:
        searchidd = ' '.join(context.args[:])
    text, notitle = dmmonecid(searchid)
    if notitle == 1:
        #update.message.reply_text('没有找到%s的cid信息，自动尝试使用/search功能搜索' %searchid)
        boxlist,stitle = dmmsearch(searchidd,'onlysearch')
        if boxlist == '選択した条件で商品は存在しませんでした':
            update.message.reply_text('没有找到 %s 的cid信息,自动搜索无结果:%s' % (searchid, boxlist))
            return
        #print(boxlist)
        firstlist = boxlist[0]
        wcid = firstlist.get('cid')
        text, notitle = dmmonecid(wcid)

        update.message.reply_markdown(text)


    else:
        update.message.reply_markdown(text)
    
        
@restricted    
@send_typing_action 
def lib(update, context):
    list1 = context.args
    url=' '.join(list1)
    #print(url)
    
    result, time = thread_javlib(url)
    text = str(result) + '\n' + str(time)
    update.message.reply_text(text)

@restricted    
@send_typing_action
def dmmvideo(update, context):
    searchid = context.args[0]
    #text = str(prevideo(searchid))
    #update.message.reply_video(text)
    text1 = str(prevideo(searchid))
    try:
        
        update.message.reply_video(text1)

    except:
        update.message.reply_text('video too large!---%s'%text1)
        text = str(prevideolow(searchid))
        update.message.reply_video(text)

@restricted      
@send_typing_action
def dmmphoto(update, context):
    searchid = context.args[0]
    #chat_id = update.message.chat_id
    urls = prephotos(searchid)
    #print(telegram.InputMediaPhoto(urls))
    #context.bot.send_media_group(chat_id,media = telegram.InputMediaPhoto(media = urls, parse_mode = telegram.ParseMode.markdown))
    #update.message.reply_media_group(media = telegram.InputMediaPhoto(urls))
    for i in urls:
        #context.bot.send_media_group(chat_id,media = telegram.InputMediaPhoto(i))
        #update.message.reply_media_group(media = telegram.InputMediaPhoto(i))
        update.message.reply_photo(i)
    #url = ','.join(urls)

@restricted    
@send_typing_action
def magnet(update, context):
    if len(context.args) == 1:
        searchid = context.args[0]
        
    else:
        searchid = ' '.join(context.args[:])
    
    result = sukebei(searchid)

    msg = long_message(update, context, result)
    
@restricted
@send_typing_action
def dmmsearchh(update, context):
    if len(context.args) == 1:
        searchstr = context.args[0]
        
    else:
        searchstr = ' '.join(context.args[:])
        
    #print(searchstr)
    
    text = dmmsearch(searchstr)
    update.message.reply_markdown(text)

@restricted
@send_typing_action 
def dmmlink(update, context):
    if len(context.args) == 1:
        searchlink = context.args[0]
        
    else:
        searchlink = ' '.join(context.args[:])
        
    #print(searchlink)
    
    text = dmmlinks(searchlink)

    msg = long_message(update, context, text)

@restricted
@send_typing_action 
def new30(update, context):
    searchlink = 'https://www.dmm.co.jp/digital/videoa/-/list/=/article=latest/limit=30/sort=date/'
    text = dmmlinks(searchlink)
    update.message.reply_markdown(text)

@restricted
@send_typing_action 
def top30(update, context):
    searchlink = 'https://www.dmm.co.jp/digital/videoa/-/list/=/limit=30/sort=ranking/'
    text = dmmlinks(searchlink)
    update.message.reply_markdown(text)

@restricted
@send_typing_action 
def cf(update, context):
    args = context.args
    cf = CloudFlare_handler(args)
    text = cf.option()
    update.message.reply_markdown(text)

def main():
    if ifproxy == True:
        updater = Updater(TOKEN, use_context=True,request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(TOKEN, use_context=True)
    
    #print(bot.get_me())
    dp = updater.dispatcher
    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("m", monthlyy))
    dp.add_handler(CommandHandler("uid", dmmid))
    dp.add_handler(CommandHandler("lib", lib))
    dp.add_handler(CommandHandler("video", dmmvideo))
    dp.add_handler(CommandHandler("photo", dmmphoto))
    dp.add_handler(CommandHandler("cid", dmmcid))
    dp.add_handler(CommandHandler("magnet", magnet))
    dp.add_handler(CommandHandler("search", dmmsearchh))
    dp.add_handler(CommandHandler("links", dmmlink))
    dp.add_handler(CommandHandler("new", new30))
    dp.add_handler(CommandHandler("top", top30))
    dp.add_handler(CommandHandler("cf", cf))
    dp.add_handler(CommandHandler('restart', restart, filters=Filters.user(user_id=LIST_OF_ADMINS[0])))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    
    
    
    main()