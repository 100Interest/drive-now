import uvicorn

from app.api.main import app as drive_now_app


def main():
    uvicorn.run(drive_now_app, host='0.0.0.0', port=7777)


if __name__ == '__main__':
    main()
