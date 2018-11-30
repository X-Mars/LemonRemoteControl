# LemonRemoteControl

### 项目介绍
基于企业微信、zabbix、ansible的服务器远程操控系统。
![1](https://github.com/X-Mars/LemonRemoteControl/blob/master/preview/1.jpeg?raw=true)
![2](https://github.com/X-Mars/LemonRemoteControl/blob/master/preview/1.jpeg?raw=true)

### 应用场景
1. zabbix 收到微信报警：tomcat 挂掉了
2. 打开 柠檬，重启对应tomcat
3. 服务恢复，收到zabbix ok信息

#### 想想看这样的场景
和女朋友 刚开始前戏，收到一个zabbix报警，这时候爬起来开电脑，岂不是很扫兴，没准还会被女友骂**没用**。

如果有了柠檬就不一样了，拿起手机，都不用拔出来，动动手指解决问题，继续和女友啪啪。

### 使用方法

##### 企业微信相关：

1. 注册企业微信 https://work.weixin.qq.com/?from=qyh_redirect
2. 创建标签，**仅允许该标签内的用户访问柠檬系统**
2. 创建应用，设置可见范围，并记录**AgentId**、**Secret**
3. 设置**网页授权及JS-SDK**，对应你的域名
4. 设置自定义菜单，跳转到url，比如：   
**https://open.weixin.qq.com/connect/oauth2/authorize?appid=dddd&redirect_uri=http%3a%2f%2fwechat.ddddd.com%2flogin%2f&response_type=code&scope=snsapi_privateinfo&agentid=1000002&state=STATE#wechat_redirect**


##### 部署应用
1. 下载应用
```shell
git clone https://github.com/X-Mars/LemonRemoteControl.git
pip3.6 install -r requirements.txt
```
2. 修改**setting.py**
```cython
WECHAT_SETTING = {
    'corp_id': '222',
    'secret': '222222',
    'agent_id': '1000002',
    'tag_id': '1'
}

ZABBIX_SETTING = {
    'home_url': 'http://zabbix.cn',
    'username': '222',
    'password': '22222'
}
```
3. 启动应用
```shell
python3.6 LemonRemoteControl/manage.py runserver 0.0.0.0:8000
```

##### 打开企业微信访问即可