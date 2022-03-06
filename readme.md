## Actions 发送消息测试 
### 通过Actions自动发送信息到钉钉机器人

1. 安装钉钉机器人

    取得机器人的webhook和secret。

2. 配置好 Python 自动运行脚本

3. 通过Actions secrets 设置传入参数（机器人的webhoo和secret）。

4. 运行时通过在脚本后添加 & {{ secrets.webhook }} ${{ secrets.secret }} 参数来传入参数给脚本。