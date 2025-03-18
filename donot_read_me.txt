
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
    Dependency install：
    #你需要先安装npm
    npm install

    start: 
    npm start
    #访问http://localhost:3000/Links 就可以看到页面
