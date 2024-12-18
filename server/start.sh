#!/bin/bash

# 检查数据库
python check_db.py

# 如果数据库检查失败，初始化数据库
if [ $? -ne 0 ]; then
    echo "Database check failed, initializing database..."
    cd ..
    npm run init-db
    cd server
fi

uvicorn main:app --host 127.0.0.1 --port 3000 --reload --log-level info
