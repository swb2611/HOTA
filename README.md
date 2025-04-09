后端配置：

    set up virtual env:

    pip install virtualenv
    which python3
    virtualenv env --python=

    start python virtual enviroment:

    . env/bin/activate

    install dependency:

    pip install -r requirements.txt

    migrate database:
    python manage.py makemigrations
    python manage.py migrate

    start server:
    python manage.py runserver

    #启动后可以测试 http://127.0.0.1:8000/api/machine-status/

前段配置：
Dependency install： #你需要先安装 npm
npm install

    start:
    npm start
    #访问http://localhost:3000/Links 就可以看到页面

Celery 服务需要 redis 数据库做 broker:

    brew services restart redis
    redis-cli ping

启动 Celery 定时任务（注意在 manage.py 目录下）：

    https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#id8
    celery -A hota worker -l debug #启动workder
    celery -A hota beat -l debug #启动定时beat scheualer
    celery -A hota flower --port-5555 #监控平台 debug用
