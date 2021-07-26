# flaskApipermission

#### 介绍
在某课网的flask课程代码基础上写的权限管理系统后端api，配合共享的前端框架使用
目前功能有规则管理，菜单管理，组管理，用户管理，部门管理
后台数据库使用mysql，日志数据库mongodb，先新建数据库，在config/secure.py下修改数据库配置

目录
app               项目文件
-api              接口文件
-block            项目目录
-config           配置文件
-libs             自定义方法
-middlewares      中间件 全局拦截
-models           orm
-static
-validators       表单验证
-view_model       视图模型基类
-web_socket       未完成
-app.py           重写json
-__init__.py
init_data         初始化数据
fake.py           初始化数据脚本
manage.py         入口文件
pipfile           项目依赖

#### 软件架构
vscode + python3.8 + pipenv


#### 安装教程
安装python3.8以上
安装虚拟环境
pip install pipenv

vscode 设置虚拟环境
pipenv --venv查看虚拟环境目录
C:\\Users\\yourpc\\.virtualenvs\\flaskapipermission-****
在vscode中 Ctrl+Shift+p
输入 settings 选择 Preferences: Open Settings (JSON)
在文件最后一行添加
"python.venvPath": "C:\\Users\\yourpc\\.virtualenvs\\flaskapipermission-****"
重启vscode，左下角可以切换环境

vscode切换到虚拟环境后，执行pipenv install 安装依赖，再右键fake.py在终端执行 初始化数据
最后右键manage.py再终端执行运行项目，就可以访问接口了


