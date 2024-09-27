# Dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 更新包列表并安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 如果上面的命令失败，尝试使用清华大学镜像源
RUN if [ $? -ne 0 ]; then \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*; \
    fi

# 复制必要的文件
COPY requirements.txt .
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/
COPY cookies.txt .

# 升级pip并安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 安装gamdl库
RUN pip install gamdl

# 创建输出目录
RUN mkdir /app/output

# 设置环境变量
ENV OUTPUT_DIR=/app/output

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "app.py"]
