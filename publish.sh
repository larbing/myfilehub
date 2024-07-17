#!/bin/bash

# 定义变量
DOCKER_CONTAINER_NAME="myfilehub"
DOCKER_IMAGE_NAME="abc7223/myfilehub"
DOCKER_TAG="latest" # 或者指定版本号，如 "v1.0"

# 函数：停止并移除旧容器
stop_and_remove_old_container() {
    echo "停止并移除旧容器..."
    docker stop $DOCKER_CONTAINER_NAME && docker rm $DOCKER_CONTAINER_NAME
}

# 函数：拉取最新的Docker镜像
pull_latest_image() {
    echo "拉取最新的Docker镜像..."
    docker pull $DOCKER_IMAGE_NAME:$DOCKER_TAG
}

# 函数：使用新镜像启动新的容器
run_new_container() {
    echo "使用新镜像启动新的容器..."
    # 这里添加您启动容器所需的参数，例如端口映射、环境变量等
    docker run --rm -d -v /data:/data -p 8080:8080 -p 8081:8081 --name myfilehub abc7223/myfilehub:latest
}

# 主程序
echo "开始更新Docker应用..."


clean_container(){
        # 检查容器是否存在
        if [ "$(docker ps -a -q -f name=$DOCKER_CONTAINER_NAME)" ]; then
                echo "找到名为 $DOCKER_CONTAINER_NAME 的容器，准备更新..."
                stop_and_remove_old_container
        else
                echo "未找到名为 $DOCKER_CONTAINER_NAME 的容器，将直接启动新容器..."
        fi
}

pull_latest_image

# 检查镜像拉取是否成功
if [ $? -eq 0 ]; then
    echo "镜像拉取成功，准备启动新容器..."
    clean_container
    run_new_container
else
    echo "镜像拉取失败，请检查网络连接和镜像名称。"
    exit 1
fi

echo "Docker应用更新脚本执行完毕。"