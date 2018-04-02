# EasyTransfer

简易的文件共享工具。利用扫描QR二维码，实现文件、消息的便捷共享。

### 原理

利用小型的flask服务在局域网内共享消息和文件。

自动生成共享文件和消息的对应URL的QR二维码,可以通过手机扫描二维码打开浏览器，查看或下载。

### 安装

只支持python3.x

依赖：click, Flask, requests

1. 克隆仓库

2. 设置文件共享目录,修改./easytransfer/config.py 中的`UPLOAD_FOLDER`,**绝对路径**

3. 利用setup.py安装 `python setup.py install`

### 使用

- 共享文件：`easytr f <需要共享的文件路径>`

- 共享消息：`easytr m <消息内容>`

- 显示主页二维码：`easytr h` 

### 效果

![效果演示gif](http://p6ift0an3.bkt.clouddn.com/easytransfer.gif)


### 参考

[sylnsfar/qrcode](https://github.com/sylnsfar/qrcode)

[claudiodangelis/qr-filetransfer](https://github.com/claudiodangelis/qr-filetransfer)

