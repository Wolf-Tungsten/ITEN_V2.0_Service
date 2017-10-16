# ITEN_V2.0：后端服务设计文档

## 一、用户系统

用于用户身份认证及全局操作的权限鉴定。

###  1. 用户数据表

在cookie中保存token，并在用户请求头中加入token作为身份认证标识

| 字段名       | 类型       | 描述                    |
| --------- | -------- | --------------------- |
| _id       | ObjectId | MongoDB索引             |
| username  | string   | 用户名                   |
| password  | string   | 密码                    |
| token     | string   | 由用户名+密码+时间戳计算SHA256得到 |
| timer     | int      | 训练时长分钟为单位             |
| privilege | int      | 权限（普通用户 = 0，管理员 = 1）  |

### API

| 路由                 | 参数                 | 返回                       | 描述                      |
| ------------------ | ------------------ | ------------------------ | ----------------------- |
| GET /auth/info     | token              | username,timer,privilege | 用户信息，用于权限鉴定和返回          |
| POST /auth/login   | username, password | token                    | 获取token                 |
| POST /auth/adduser | username, password | flag                     | 添加新用户                   |
| PUT /auth/password | username, password | Flag                     | 将username的密码修改为password |



## 二、硬件模型系统

搭建网球机在线模型。用户对网球机的操作映射到网球机模型；网球机向服务器获取信息时从网球机模型获取数据并执行相应的硬件操作。

### 1. 硬件模型

该模型与用户界面及硬件双向绑定。

用户请求设置state、train_id、train_amount参数，获取state、train_name、train_amount、train_count参数，如果有需要向command头部添加需要执行的命令代号

硬件请求设置state、train_name、train_amount、train_count参数，获取state、train_id、train_name参数，网球机每次请求从command中取出一个命令代号分析并执行

| 属性名          | 类型     | 描述                                       |
| ------------ | ------ | ---------------------------------------- |
| id           | string | 网球机全局标识id                                |
| state        | string | 工作状态（deploying-用户部署任务，working-正在工作，pause-暂停工作，stop） |
| command      | queue  | 待执行命令                                    |
| train_name   | string | 训练模式名称                                   |
| train_amount | int    | 训练总数                                     |
| train_count  | Int    | 训练进度                                     |
| train_id     | string | 训练模式                                     |
| alive        | Int    | 存活时间戳                                    |



### 2. 用户-网球机字典

以用户id为键，网球机id为值作为值。

通过用户id判断当前使用网球机以获取相关状态、修改状态。

### 3. 硬件参数数据表

网球机将整个球场抽象16个点，每个点使用上转速、下转速、水平角度、俯仰角度作为依据进行发球。

由于网球机机械结构可能存在差异，故应对不同机器进行校准，校准数据存储于服务器数据库，每次网球机上电向服务器获取参数。

| 字段名称      | 类型       | 描述          |
| --------- | -------- | ----------- |
| _id       | ObjectId | MongoDB索引   |
| id        | string   | 网球机id       |
| arguments | string   | 参数描述json字符串 |

参数描述json字符串

```json
{
  "machineA":{
        "point1":{
          "upspeed":int,
          "downspeed":int,
          "vertical":int,
          "horizontal":int
        },
        "point2":{
          "upspeed":int,
          "downspeed":int,
          "vertical":int,
          "horizontal":int
        },
  		...
  	},
    "machineB":{
        "point1":{
          "upspeed":int,
          "downspeed":int,
          "vertical":int,
          "horizontal":int
        },
        "point2":{
          "upspeed":int,
          "downspeed":int,
          "vertical":int,
          "horizontal":int
        },
      	...
    }
}
```

### Web API

| 路由                     | 参数                        | 返回                                       | 描述                               |
| ---------------------- | ------------------------- | ---------------------------------------- | -------------------------------- |
| GET /hardware/state    |                           | has, id, state, train_name, train_amount, train_count | 获取用户当前状态[检查是否有正在使用的网球机->如果有返回状态] |
| GET /hardware/free     |                           | list                                     | 获取状态为free，并且存活的网球机               |
| POST /hardware/deploy  | id，train_id, train_amount | flag                                     | 更新用户-网球机字典->更新网球机模型状态            |
| POST /hardware/pause   |                           | flag                                     | 查询当前使用网球机id->更新网球机模型             |
| POST /hardware/stop    |                           | flag                                     | 查询当前使用网球机id->更新网球机模型             |
| POST /hardware/command | command                   | flag                                     | 查询当前使用网球机id->更新网球机模型             |

### Hardware API

| 路由                      | 参数                                       | 返回                                       | 描述                                       |
| ----------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| POST /hardware/active   | id, state, train_id, train_name, train_amount, train_count | state, train_id, train_amount, train_count，command | 更新网球机alive时间戳->如果模型状态为deploy，机器状态不是working，不更新参数，将模型参数返回，其他情况直接更新模型状态->查询用户id->下发 |
| GET /hardware/arguments | id                                       | arguments描述json                          | 网球机上电先行请求参数，更新参数模型                       |



## 三、训练模式系统

当网球机获取状态为deploying时，按照train_id向服务器请求训练模式

### 1.训练模式数据表

| 字段名称       | 类型       | 描述            |
| ---------- | -------- | ------------- |
| _id        | ObjectId | MongoDB索引     |
|            |          |               |
| train_name | String   | 训练模式名称，用于显示   |
| train_data | String   | json字符串描述训练模式 |

### 2. 训练模式描述json

```
{
  "type":<"cycle"-循环模式>|<"ai"-人工智能模式>,
  "cycle":[
    {
      "machine":<"A"-机器A发球>|<"B"-机器B发球>,
      "point":int, //0-16表示发球方向点
      "director":int, //代表回球指导
    }，
    ...
  ],//如果训练模式类型为cycle，则循环执行cycle列表描述的所有发球及指导
  "ai":{}//目前开发阶段不能确定今后AI如何设计，故预留此字段
}
```

### API

| 路由                       | 参数                         | 返回                                       | 描述                  |
| ------------------------ | -------------------------- | ---------------------------------------- | ------------------- |
| GET /trainmode/available |                            | {avaliable_list:[{train_name,train_id}]} | 获取所有可用训练模式id及名称     |
| GET /trainmode/data      | id                         | {train_name, train_data}                 | 获取当前id所指定训练模式的名称和数据 |
| POST /trainmode          | id, train_name, train_data | Flag                                     | 添加训练模式              |
|                          |                            |                                          |                     |

## 四、精彩镜头回放

实现用户查看使用过程中精彩镜头功能

### 1. 用户视频表

| 字段名称      | 类型       | 描述        |
| --------- | -------- | --------- |
| _id       | ObjectId | MongoDB索引 |
| user_id   | String   | 用户ID      |
| video_url | String   | 视频URL     |

