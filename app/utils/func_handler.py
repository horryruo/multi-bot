import  logging, telegram, time
#from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler
from app.utils.loadini import read_config
from functools import wraps



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE,GIRL,ACG,GITUPDATE = range(4)


class Config(object):
    def  __init__(self):
        self.allconfig = read_config()
        self.ifproxy = self.allconfig['ifproxy'] 
        self.proxy = self.allconfig['proxy'] 
        self.iftb = self.allconfig['tb'] 
        self.TOKEN = self.allconfig['token']
        users = self.allconfig['userid'] 
        userid = users.split(',')
        userss = []
        #userid = ','.join(userid)
        for i in userid:
            userss.append(int(i))
        #print(userid)
        #userids = ','.join(userss)
        self.LIST_OF_ADMINS = userss
        self.REQUEST_KWARGS={
                # "USERNAME:PASSWORD@" is optional, if you need authentication:
            'proxy_url': 'http://%s/'%self.proxy,
        }   
config = Config()

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    #update.message.reply_text(str(update.message.text))
    try:
        update.message.reply_text(str(context.error))
    except:
        update.callback_query.edit_message_text(str(context.error))

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
        if user_id not in config.LIST_OF_ADMINS:
            error = "Unauthorized access denied for you!!you user id:{}.".format(user_id)
            update.message.reply_markdown(error)
            print(error)
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def long_message(update, context, text: str,mtype):
    max_length = telegram.constants.MAX_MESSAGE_LENGTH
    if len(text) <= max_length:
        if mtype=='markdown':
            return update.message.reply_markdown(text)
        else:
            return update.message.reply_text(text)

    parts = []
    while len(text) > max_length:
        last = text[:max_length].rfind('=>')
        if last ==  -1:
            last1 = text[:max_length].rfind(',')
            cut1 = last1 +1
            parts.append(text[:cut1])
            text = text[cut1:]
        elif last == 1:
            last1 = text[:max_length].rfind(',')
            cut1 = last1 +1
            parts.append(text[:cut1])
            text = text[cut1:]
        elif last <= 100:
            last1 = text[:max_length].rfind(',')
            cut1 = last1 +1
            parts.append(text[:cut1])
            text = text[cut1:]
        else:
            cut = last - 1
            parts.append(text[:cut])
            text = text[cut:]
    parts.append(text)
    msg = None
    for part in parts:
        try:
            update.message.reply_markdown(part)
        except:
            update.message.reply_text(part)
        time.sleep(3)
    return msg
def split_list(init_list, children_list_len):
    _list_of_groups = zip(*(iter(init_list),) *children_list_len)
    end_list = [list(i) for i in _list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list