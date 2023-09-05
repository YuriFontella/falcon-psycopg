import uvicorn, os, multiprocessing

env = os.environ.get('ENV', 'development')

ssl_keyfile = None
ssl_certfile = None
reload = True

if env == 'production':
    ssl_keyfile = ''
    ssl_certfile = ''
    reload = False

if __name__ == "__main__":
    uvicorn.run(
        app='src.main:app',
        host='0.0.0.0',
        port=6500,
        ssl_certfile=ssl_certfile,
        ssl_keyfile=ssl_keyfile,
        reload=reload,
        workers=multiprocessing.cpu_count() // 2 + 1
    )