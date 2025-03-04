# (c) Code-x-Mania
import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from .bot import StreamBot
from .vars import Var
from aiohttp import web
from .server import web_server
from .utils.keepalive import ping_server
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

ppath = "Code_X_Mania/bot/plugins/*.py"
files = glob.glob(ppath)
StreamBot.start()
loop = asyncio.get_event_loop()


async def start_services():
    print('\n')
    print('------------------- Initalizing Telegram Bot -------------------')
    
    print('----------------------------- DONE -----------------------------')
    print('\n')
    print('--------------------------- Importing ---------------------------')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"Code_X_Mania/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["Code_X_Mania.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    if Var.ON_HEROKU:
        print('------------------ Starting Keep Alive Service ------------------')
        print('\n')
        scheduler = BackgroundScheduler()
        scheduler.add_job(ping_server, "interval", seconds=1200)
        scheduler.start()
    print('-------------------- Initalizing Web Server -------------------------')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    print('----------------------------- DONE ---------------------------------------------------------------------')
    print('\n')
    print('---------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------------------------------------------------------------------')
    print('https://github.com/SkullGG-Ui follow me for new bots')
    print('---------------------------------------------------------------------------------------------------------')
    print('\n')
    print('----------------------- Service Started -----------------------------------------------------------------')
    print('                        bot =>> {}'.format((await StreamBot.get_me()).first_name))
    print('                        server ip =>> {}:{}'.format(bind_address, Var.PORT))
    print('                        Owner =>> {}'.format((Var.OWNER_USERNAME)))
    if Var.ON_HEROKU:
        print('                        app runnng on =>> {}'.format(Var.FQDN))
    print('---------------------------------------------------------------------------------------------------------')
    print('Give a star to my repo https://github.com/SkullGG-Ui/FilestreambotX  also follow me for new bots')
    print('---------------------------------------------------------------------------------------------------------')
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')
