#!/bin/bash

# 切换到应用目录
cd /home/site/wwwroot

# 安装依赖
pip install -r requirements.txt

cd /home/site/wwwroot/myproject

# 启动Gunicorn --chdir /home/site/wwwroot/myproject
gunicorn --bind=0.0.0.0:8000 myproject.wsgi

#cd /home/site/wwwroot/myproject
