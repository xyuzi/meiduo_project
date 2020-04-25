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

# 相关配置

`进入hosts添加->127.0.0.1	www.meiduo.site`

`进入libs/yuntongxun/cpp_sms.py -> 添加云通讯相关配置说明：`

````
https://www.yuntongxun.com/
主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID`
_accountSid = ''

说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = ''

请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = ''
````
# start:

`启动redis，启动mysql`

`进入front_end_pc执行 --> python3 -m http.server 8080`

`进入meiduo_mall执行 --> python3 manage.py runserver`
