import uvicorn

from src.api.main import app as drive_now_app
from src.config.logging import setup_logging


def main():
    setup_logging()
    uvicorn.run(drive_now_app, host='0.0.0.0', port=7777)


if __name__ == '__main__':
    main()
