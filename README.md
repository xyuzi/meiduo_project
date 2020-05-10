# meiduo_project
美多商城


# Package:

`详情导入使用`
script/requirements.txt

`本地utils文件夹安装`

`pip install fdfs_client-py-master.zip `

# 相关配置

`进入hosts添加->127.0.0.1	www.meiduo.site`

[https://www.yuntongxun.com/](https://www.yuntongxun.com/)

`进入cpp_sms.py -> 添加云通讯相关配置：`


````

dev.py/pord.py设置
QQ登录参数 需要配置
发送邮件的邮箱 需要配置
utils/fastdfs/client.conf --> 修改配置文件地址和ip

第一次需要手动生成索引表
python manage.py rebuild_index

uwsgi.ini 需要配置

其他配置可看read.txt
````
# start:

`启动redis,启动mysql,启动mysql从机`

`启动docker下启动(mysql-slave ,elasticsearch, storage, tracker)`

`进入front_end_pc执行 --> python3 -m http.server 8080`

`生成迁移文件: `

`进行迁移: `

```
进入meiduo_mall执行 --> python3 manage.py runserver

或者在看见uwsgi.ini地方命令行-->  uwsgi --ini uwsgi.ini```
