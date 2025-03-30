#!/bin/bash

# 切换到 backend 目录
cd myproject

# 安装依赖
pip install -r requirements.txt

# 激活虚拟环境 (如果你使用了虚拟环境)
# source venv/bin/activate   # 如果你有虚拟环境，取消注释这一行

# 运行 Django 项目，使用 gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
