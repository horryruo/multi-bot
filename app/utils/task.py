import telegram, os, time, re 
from telegram.ext import ConversationHandler
from app.utils.monthly import monthly_thread
from app.utils.jav_thread import thread_javlib
from app.utils.magnet import sukebei
from app.utils.func_requests import get_file
from app.utils.dmm import dmm_thread, prevideo, prephotos, dmmonecid, dmmsearch, dmmlinks, truevideo, dmmsearchall, precid
from app.utils.faleno import Faleno
from app.utils.playerlist import Javmost
from app.utils.shell import Bashshell
from app.utils.cloudflare import CloudFlare_handler
from app.utils.get_update import Version
from app.utils.identify import girl, acg
from app.utils import func_handler





@func_handler.send_typing_action
def start(update, context):
    text = '''
    **
    欢迎使用imulti bot，请输入/help查看指令
    **
    '''
    #print(telegram.constants.MAX_MESSAGE_LENGTH)
    update.message.reply_markdown(text)

@func_handler.send_typing_action
def help(update, context):
    text = '''
    *bot命令帮助*
    *start* - `欢迎  `
    *help* - `帮助`
    *m* - `查询是否ikoa月额，num/cid皆可，可批量查询，半角逗号分隔   /m ssni-520,ssni-521`
    *uid* - `1、查询女优在dmm所有uid，需女优在dmm的数字id  /uid 2333;2、查询list链接所有uid，需完整dmm链接`
    *lib* - `(目前不可用)查询女优在library所有番号，需女优页面完整https链接  /lib https://*****`
    *video* - `dmm预览视频，cid(准确)，num(可能查询不到),dmm没有时会从faleno和sod寻找`
    *photo* - `dmm预览图片，cid(准确)，num(可能查询不到)，dmm没有时会从faleno寻找`
    *cid* -  `查询番号具体信息，cid(准确)，num(可能查询不到) `
    *magnet* -  `搜索关键词在sukebei（磁力）`
    *search* -  `搜索关键词在dmm，dmm官方支持正则，例如当长字符无结果，可利用空格分割`
    *all* -  `搜索关键词在dmm所有区域的内容，dmm官方支持正则，例如当长字符无结果，可利用空格分割`
    *faleno* - `搜索faleno，支持名字，标题，不支持cid、num(官方不支持),二级命令功能看下面`
    *stream* - `获取播放直链,只支持num`
    *sh* - `/sh bash命令,可空格,如需一次执行多条命令用;分隔即可,如:/sh cd /root;ls`
    *kill* - `杀死sh命令,tg回复需停止的消息发送命令即可`
    *links* -  `输入dmm list链接获取内容`
    *face* - `根据提示发送图片进行人脸识别`
    *new* -  `dmm new video `
    *top* -  `dmm hot video`
    *update* - `更新机器人`
    *restart* - `重启机器人`
    *cancel* - `处在对话命令内时，提前结束对话`
    *faleno* - `faleno 输入命令查看二级指令`
    *cf* - `cloudflare 输入命令查看二级指令`
    *stream* - `stream 输入命令查看二级指令`
    '''
    update.message.reply_markdown(text)

@func_handler.restricted
@func_handler.send_typing_action 
def shell(update, context):
    #print(update)
    bashshell = Bashshell(update,context)
    bashshell.task_buffer()
    
@func_handler.restricted
@func_handler.send_typing_action 
def killshell(update, context):
    reply_id = update.message.reply_to_message.message_id
    content = update.effective_message.text
    if "/kill" == content :
        func_handler.Task.Msg[reply_id]=1
    


@func_handler.restricted
@func_handler.send_typing_action 
def monthlyy(update, context):
    #print(context.args)
    chat_id=update.message.chat_id
    id = context.args
    #print(id)
    idlist = ','.join(id)
    searchlist1 = idlist.split(',')
    leng3 = len(searchlist1)
    update.message.reply_text('正在查询%s个...请稍候......' %leng3)
    
    mon,leng,nomon,leng1,time,tbb,tbbb,noresult,noresultleng = monthly_thread(idlist)
    tb = str(tbb)
    usetime = '耗时:' + time + '秒'
    if leng == 0:
        if leng1 == 0:
            
            noresult = '无结果  (%s) => %s' %(noresultleng,noresult)
            msg = func_handler.long_message(update, context, noresult)
        else:
            result1 = '非月额list (%s) => %s' %(leng1,nomon)
            if func_handler.Config.iftb == 'true':
                msg = func_handler.long_message(update,context,tb)
            msg = func_handler.long_message(update,context,result1)
            if noresultleng>0:
                
                noresult = '无结果  (%s) => %s' %(noresultleng,noresult)
                msg = func_handler.long_message(update, context, noresult)
            update.message.reply_text(usetime)
    else:
        if leng1 == 0:
            if func_handler.Config.iftb == 'true':
                msg = func_handler.long_message(update,context,tb)
            result = '月额list (%s) => %s' %(leng,mon)
            msg = func_handler.long_message(update,context,result)
            if noresultleng>0:
                
                noresult = '无结果  (%s) => %s' %(noresultleng,noresult)
                msg = func_handler.long_message(update, context, noresult)
            update.message.reply_text(usetime)
        else:
            result = '月额list (%s) => %s' %(leng,mon)
            result1 = '非月额list (%s) => %s' %(leng1,nomon)
            if func_handler.Config.iftb == 'true':
                msg = func_handler.long_message(update,context,tb)
            msg = func_handler.long_message(update,context,result)
            msg = func_handler.long_message(update,context,result1)
            if noresultleng>0:
                
                noresult = '无结果  (%s) => %s' %(noresultleng,noresult)
                msg = func_handler.long_message(update, context, noresult)
            update.message.reply_text(usetime)
    
@func_handler.restricted
@func_handler.send_typing_action  
 
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
    msg = func_handler.long_message(update,context,result)

    
@func_handler.restricted
@func_handler.send_typing_action
def dmmcid(update,context):
    allid = ' '.join(context.args[:])
    searchidlist = allid.split(',')
    for cid in searchidlist:
        searchidd = cid.replace('-',' ')
        num = re.findall(r'(\w+_?\w+[a-zA-Z]+)-?[ ]?(\d{1,}\w{0,})', searchidd)
        if num != []:
            searchidd = ' '.join(num[0])

        text, notitle = dmmonecid(cid)
        if notitle == 1:
            boxlist,stitle = dmmsearch(searchidd,'onlysearch')
            typee = False
            if boxlist == '選択した条件で商品は存在しませんでした':
                boxlist,stitle = dmmsearchall(searchidd,'onlysearch')
                typee = True
                if boxlist == 'に一致する商品は見つかりませんでした。':
                    update.message.reply_text('没有找到 %s 的cid信息,自动搜索无结果:%s' % (cid, boxlist))
                    continue 
        #print(boxlist)
            firstlist = boxlist[0]
            wcid = firstlist.get('cid')
            if typee:
                text = precid(wcid)
                update.message.reply_markdown(text)
                continue
            text, notitle = dmmonecid(wcid)

            update.message.reply_markdown(text)


        else:
            update.message.reply_markdown(text)
        time.sleep(1)

@func_handler.restricted    
@func_handler.send_typing_action 
def stream(update, context):
    args = context.args
    javmost = Javmost(args)
    result = javmost.option()
    msg = func_handler.long_message(update,context,result,'markdown')
@func_handler.restricted    
@func_handler.send_typing_action 
def lib(update, context):
    list1 = context.args
    url=' '.join(list1)
    #print(url)
    
    result, time = thread_javlib(url)
    text = str(result) + '\n' + str(time)
    msg = func_handler.long_message(update,context,text)

@func_handler.restricted    
@func_handler.send_typing_action
def dmmvideo(update, context):
    searchid = context.args[0]
    if len(context.args) == 1:
        searchidd = context.args[0]
        num = re.findall(r'(\w+_?\w+[a-zA-Z]+)-?[ ]?(\d{1,}\w{0,})', searchidd)
        if num != []:
            searchidd = ' '.join(num[0])
        searchidd = searchidd.replace('-',' ')
    else:
        searchidd = ' '.join(context.args[:])
        num = re.findall(r'(\w+_?\w+[a-zA-Z]+)-?[ ]?(\d{1,}\w{0,})', searchidd)
        if num != []:
            searchidd = ' '.join(num[0])
        
    
    boxlist,stitle = dmmsearch(searchidd,'onlysearch')
    if boxlist == '選択した条件で商品は存在しませんでした':
        faleno = Faleno(context.args)
        searchid = searchidd.replace(' ','')
        try:
            video = faleno.video(searchid)
            update.message.reply_text('视频资源来自faleno,超出telegram大小限制,复制链接到浏览器查看:\n'+ video)
            return
        except:
            try:
                numid= '-'.join(num[0])
                video = faleno.sod(numid)
                with open("upload.mp4", "wb") as f:
                    f.write(video)
                f.close()
                update.message.reply_text('视频资源来自sod,画质较差,正在上传,请稍后')
                update.message.reply_video(open('upload.mp4', 'rb'))
                os.remove("upload.mp4")
                #update.message.reply_video(video)
                return
            except Exception as e:
                func_handler.logger.warning(str(e))
        boxlist,stitle = dmmsearchall(searchidd,'onlysearch')
        if boxlist == 'に一致する商品は見つかりませんでした。':
            update.message.reply_text('没有找到 %s 预览视频'%searchid)
            return
    firstlist = boxlist[0]
    searchid = firstlist.get('cid')
    try:
        result = str(truevideo(searchid))
    except Exception as e:
        #func_handler.logger.error(traceback.format_exc())
        #func_handler.logger.warning(str(e))
        func_handler.logger.warning('尝试使用selenium引擎失败')
        result = str(prevideo(searchid))
    try:
        update.message.reply_video(result)
    except:
        result_hd = result
        update.message.reply_text('原视频超出telegram大小限制，将发送低画质版本，可复制原画质链接到浏览器查看!---%s'%result_hd)
        result = result.replace('mhb','dmb')
        '''
        try:
            file = get_file(result_hd)
            with open("upload.mp4", "wb") as f:
                for chunk in file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            f.close()
            update.message.reply_video(open('upload.mp4', 'rb'))
            os.remove("upload.mp4")
        except:
            pass'''
        try:
            update.message.reply_video(result)
        except:
            result = result.replace('dmb','sm')
            update.message.reply_video(result)

@func_handler.restricted      
@func_handler.send_typing_action
def dmmphoto(update, context):
    searchid = context.args[0]
    #chat_id = update.message.chat_id
    searchurl = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={}/'.format(searchid)
    list_of_urls = prephotos(searchurl)
    if list_of_urls == []:
        if len(context.args) == 1:
            searchidd = context.args[0]
            num = re.findall(r'([a-zA-Z]+)-?[ ]?(\d{1,})', searchidd)
            if num != []:
                searchidd = ' '.join(num[0])
            searchidd = searchidd.replace('-',' ')
        else:
            searchidd = ' '.join(context.args[:])
            num = re.findall(r'([a-zA-Z]+)-?[ ]?(\d{1,})', searchidd)
            if num != []:
                searchidd = ' '.join(num[0])
        boxlist,stitle = dmmsearch(searchidd,'onlysearch')
        dmm_have = True
        s_all = False
        if boxlist == '選択した条件で商品は存在しませんでした':
            boxlist,stitle = dmmsearchall(searchidd,'onlysearch')
            s_all = True
            if boxlist == 'に一致する商品は見つかりませんでした。':
                dmm_have = False
                faleno = Faleno(context.args)
                try:
                    list_of_urls = faleno.photo(''.join(num[0]))
                except:
                    update.message.reply_text('没有找到 %s 预览图片'%searchid)
                    return
        #print(boxlist)
        if dmm_have:
            firstlist = boxlist[0]
            wcid = firstlist.get('cid')
            if s_all:
                searchurl = 'https://www.dmm.co.jp/mono/dvd/-/detail/=/cid={}/'.format(wcid)
            else:
                searchurl = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={}/'.format(wcid)
            list_of_urls = prephotos(searchurl)
    try:
        if len(list_of_urls)<=10:
            media_group = []
            for number, url in enumerate(list_of_urls):
                media_group.append(telegram.InputMediaPhoto(media=url, caption="Photos" + str(number)))
            update.message.reply_media_group(media=media_group)
        else:
            list_of_urls = func_handler.split_list(list_of_urls,10) 
            for i in list_of_urls:
                media_group = []
                for number, url in enumerate(i):
                #print(telegram.InputMediaPhoto(media=url, caption="Photos" + str(number)))
                    media_group.append(telegram.InputMediaPhoto(media=url, caption="Photos" + str(number)))
            #print(media_group)
                update.message.reply_media_group(media=media_group)
    except Exception as e:
        text='发送照片组失败，失败原因：%s，转为单张图片发送'%e
        update.message.reply_markdown(text)
        for url in list_of_urls:
            try:
                update.message.reply_photo(url)
                time.sleep(0.5)
            except:
                text='造成发送失败的图片链接：%s'%url
                update.message.reply_markdown(text)
                continue
@func_handler.restricted    
@func_handler.send_typing_action
def magnet(update, context):
    if len(context.args) == 1:
        searchid = context.args[0]
        num = re.findall(r'([a-zA-Z]+)-?[ ]?(\d{1,})', searchid)
        if num != []:
            searchid = ' '.join(num[0])
    else:
        searchid = ' '.join(context.args[:])
    
    result = sukebei(searchid)

    msg = func_handler.long_message(update, context, result,'markdown')
    
@func_handler.restricted
@func_handler.send_typing_action
def dmmsearchh(update, context):
    if len(context.args) == 1:
        searchstr = context.args[0]
        
    else:
        searchstr = ' '.join(context.args[:])
        
    #print(searchstr)
    
    text = dmmsearch(searchstr)
    msg = func_handler.long_message(update,context,text,'markdown')

@func_handler.restricted
@func_handler.send_typing_action
def searchall(update,context):
    if len(context.args) == 1:
        searchstr = context.args[0]
        
    else:
        searchstr = ' '.join(context.args[:])
        
    #print(searchstr)
    
    text = dmmsearchall(searchstr)
    msg = func_handler.long_message(update,context,text,'markdown')

@func_handler.restricted
@func_handler.send_typing_action 
def dmmlink(update, context):
    if len(context.args) == 1:
        searchlink = context.args[0]
        
    else:
        searchlink = ' '.join(context.args[:])
        
    #print(searchlink)
    
    text = dmmlinks(searchlink)

    msg = func_handler.long_message(update, context, text,'markdown')

@func_handler.restricted
@func_handler.send_typing_action 
def new30(update, context):
    searchlink = 'https://www.dmm.co.jp/digital/videoa/-/list/=/article=latest/limit=30/sort=date/'
    text = dmmlinks(searchlink)
    msg = func_handler.long_message(update,context,text,'markdown')

@func_handler.restricted
@func_handler.send_typing_action 
def top30(update, context):
    searchlink = 'https://www.dmm.co.jp/digital/videoa/-/list/=/limit=30/sort=ranking/'
    text = dmmlinks(searchlink)
    msg = func_handler.long_message(update,context,text,'markdown')

@func_handler.restricted
@func_handler.send_typing_action 
def faleno(update, context):
    args = context.args
    faleno = Faleno(args)
    result = faleno.option()
    msg = func_handler.long_message(update,context,result,'markdown')
@func_handler.restricted
@func_handler.send_typing_action 
def cf(update, context):
    args = context.args
    cf = CloudFlare_handler(args)
    text = cf.option()
    update.message.reply_markdown(text)
@func_handler.restricted
@func_handler.send_typing_action 
def getupdate(update, context):
    repo = Version('https://github.com/horryruo/multi-bot.git')
    updatetime = repo.get_time()
    text = '最新版本：{} (UTC+8)'.format(updatetime)
    keyboard = [
        [
            telegram.InlineKeyboardButton('更新程序',callback_data="goupdate"),
            telegram.InlineKeyboardButton('取消',callback_data="cancel"),
        ],
        ]
    update.message.reply_markdown(text,reply_markup=telegram.InlineKeyboardMarkup(keyboard))
    
    return func_handler.GITUPDATE

def gitupdate(update, context):
    repo = Version('https://github.com/horryruo/multi-bot.git')
    try:
        pull = repo.pull()
    except Exception as e:
        pull = str(e)
        func_handler.logger.warning(str(e))
    matchline = re.search( r'file changed|Already|merge|files changed', pull, re.M|re.I)
    #print(matchline)
    if matchline:
        matchline=matchline.group()
        if matchline == 'Already':
            update.callback_query.edit_message_text('版本已是最新，无需更新\n'+ str(pull))
        elif matchline == 'file changed' or 'files changed':
            update.callback_query.edit_message_text('更新完成，请输入/restart 重启程序完成更新,更新日志：\n'+ str(pull))
        elif matchline == 'merge':
            update.callback_query.edit_message_text('你可能修改过项目文件，无法自动更新，请手动解决或重新下载程序,错误内容:\n'+ str(pull))
    else:
        update.callback_query.edit_message_text('error:\n'+ str(pull))
        
    return ConversationHandler.END
@func_handler.restricted
@func_handler.send_typing_action     
def startface(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton('识别女优',callback_data="girl"),
            telegram.InlineKeyboardButton('识别二次元图片(未完成)',callback_data="acg"),
        ],
        [
            telegram.InlineKeyboardButton('取消',callback_data="cancel"),
        ],
        ]
    update.message.reply_text(
        '选择你要识别图片的类型',
        reply_markup=telegram.InlineKeyboardMarkup(keyboard),
    )
    return func_handler.CHOOSE
def choosegirl(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text('请发送图片',)

    return func_handler.GIRL
def chooseacg(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text('请发送图片',)

    return func_handler.ACG
@func_handler.send_typing_action  
def girl_ide(update, context):
    try:
        photo_file = update.message.effective_attachment.get_file()
    except:
        photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text('正在识别，请稍候')
    result = girl()
    msg = func_handler.long_message(update, context, result,'markdown')
    os.remove("user_photo.jpg")
    return ConversationHandler.END
@func_handler.send_typing_action  
def acg_ide(update, context):
    try:
        photo_file = update.message.effective_attachment.get_file()
    except:
        photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text('本功能未完成，请等待作者咕咕咕')

    return ConversationHandler.END
def cancel(update, context):
    update.message.reply_text('已取消')

    return ConversationHandler.END

def cancell(update, context):
    update.callback_query.edit_message_text('已取消')

    return ConversationHandler.END

