# meiduo_project
美多商城


# Package:

`django == 2.2.5`

`django-redis == 4.11.0`

`django-cors-headers == 3.2.1`

`pymysql == 0.9.3`

`celery == 4.4.2 `

`QQLoginTool == 0.3.0 `

`itsdangerous == 1.1.0`

`mutagen == 1.44.0`

`requests == 2.23.0 `

`本地utils文件夹安装`

`pip install fdfs_client-py-master.zip `

# 相关配置

`进入hosts添加->127.0.0.1	www.meiduo.site`

`进入libs/yuntongxun/cpp_sms.py -> 添加云通讯相关配置说明：`

[https://www.yuntongxun.com/](https://www.yuntongxun.com/)
````
主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID`
_accountSid = ''

说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = ''

请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = ''
````
````
dev.py设置
# QQ登录参数
# 申请的 客户端id
QQ_CLIENT_ID = ''
# 申请的 客户端秘钥
QQ_CLIENT_SECRET = ''

# 发送邮件的邮箱
EMAIL_HOST_USER = ''
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = ''
# 收件人看到的发件人
EMAIL_FROM = '随便写<这里写显示的邮箱>'

utils/fastdfs/client.conf --> 修改配置文件地址和ip
````
# start:

`启动redis，启动mysql，启动FastDFS(docker下启动)`

`进入front_end_pc执行 --> python3 -m http.server 8080`

`进入meiduo_mall执行 --> python3 manage.py runserver`
