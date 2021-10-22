# -*- coding: utf-8 -*-
import os, sys
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from app.utils import func_handler, task




        
def main():
    if func_handler.config.ifproxy == 'true':
        updater = Updater(func_handler.config.TOKEN, use_context=True,request_kwargs=func_handler.config.REQUEST_KWARGS)
    else:
        updater = Updater(func_handler.config.TOKEN, use_context=True)
    
    #print(bot.get_me())
    dp = updater.dispatcher
    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text('Bot 正在重启，请等待5~10秒')
        Thread(target=stop_and_restart).start()

    dp.add_handler(CommandHandler("start", task.start))
    dp.add_handler(CommandHandler("help", task.help))
    dp.add_handler(CommandHandler("m", task.monthlyy))
    dp.add_handler(CommandHandler("uid", task.dmmid))
    dp.add_handler(CommandHandler("lib", task.lib))
    dp.add_handler(CommandHandler("video", task.dmmvideo))
    dp.add_handler(CommandHandler("photo", task.dmmphoto))
    dp.add_handler(CommandHandler("cid", task.dmmcid))
    dp.add_handler(CommandHandler("magnet", task.magnet))
    dp.add_handler(CommandHandler("search", task.dmmsearchh))
    dp.add_handler(CommandHandler("links", task.dmmlink))
    dp.add_handler(CommandHandler("new", task.new30))
    dp.add_handler(CommandHandler("faleno", task.faleno))
    dp.add_handler(CommandHandler("top", task.top30))
    dp.add_handler(CommandHandler("cf", task.cf))
    dp.add_handler(CommandHandler("all", task.searchall))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('face',task.startface),
            CommandHandler('update',task.getupdate),
        ],
        states={
            func_handler.CHOOSE:[
                CallbackQueryHandler(task.choosegirl, pattern="girl"),
                CallbackQueryHandler(task.chooseacg, pattern="acg"),
                CallbackQueryHandler(task.cancell, pattern="cancel"),
                ],
            func_handler.GIRL:[MessageHandler(Filters.photo|Filters.document,task.girl_ide)],
            func_handler.ACG:[MessageHandler(Filters.photo|Filters.document,task.acg_ide)],
            func_handler.GITUPDATE:[
                CallbackQueryHandler(task.gitupdate, pattern="goupdate"),
                CallbackQueryHandler(task.cancell, pattern="cancel"),
                ],
        },
        fallbacks=[CommandHandler('cancel',task.cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('restart', restart, filters=Filters.user(user_id=func_handler.config.LIST_OF_ADMINS[0])))
    dp.add_error_handler(func_handler.error)
    updater.start_polling()
    func_handler.logger.info("iMulti-bot started")
    updater.idle()

if __name__ == '__main__':
    main()
