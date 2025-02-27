import asyncio
import logging

from src.app import AsyncAppCtk

app = AsyncAppCtk(title="ParserUsersTelegram", width=500, height=600, fg_color="#0D0E0D")


def main():
    app.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        logging.exception(e)

