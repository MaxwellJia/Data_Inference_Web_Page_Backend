#!/bin/bash

# 切换到应用目录
cd /home/site/wwwroot

# 安装依赖
pip install -r requirements.txt

# 启动Gunicorn
gunicorn --bind=0.0.0.0:8000 myproject.myproject.wsgi --chdir /home/site/wwwroot
