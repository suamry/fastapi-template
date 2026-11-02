#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import uvicorn
from path import Path

from app.api.register import register_app
from app.common.log import log
from app.config.conf import settings

app = register_app()

if __name__ == '__main__':
    try:
        log.info(
            """\n
 /$$$$$$$$                   /$$      /$$$$$$  /$$$$$$$  /$$$$$$
| $$_____/                  | $$     /$$__  $$| $$__  $$|_  $$_/
| $$    /$$$$$$   /$$$$$$$ /$$$$$$  | $$  | $$| $$  | $$  | $$  
| $$$$$|____  $$ /$$_____/|_  $$_/  | $$$$$$$$| $$$$$$$/  | $$  
| $$__/ /$$$$$$$|  $$$$$$   | $$    | $$__  $$| $$____/   | $$  
| $$   /$$__  $$ |____  $$  | $$ /$$| $$  | $$| $$        | $$  
| $$  |  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$| $$       /$$$$$$
|__/   |_______/|_______/    |___/  |__/  |__/|__/      |______/

            """
        )
        log.info(f'🚀 FastAPI start: {settings.TITLE} {settings.VERSION}')
        log.info(f'🚀 FastAPI API docs: http://{settings.UVICORN_HOST}:{settings.UVICORN_PORT}{settings.DOCS_URL}')
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
            log_config=os.path.join(Path(__file__).parent, "config", "uvicorn_log_config.json"),
            access_log=False,
            workers=settings.UVICORN_WORKERS
        )
    except Exception as e:
        log.error(f'❌ FastAPI start filed: {e}')
