# auto-build
redmine+jenkins auto build python scripts

redmine 新增三个字段

romid：版本号
build：该版本是否编译的标致
buildtype：user版本或者debug版本

运行该脚本：需要安装必要的python组件：

sudo apt-get install libmysqlclient-dev libmysqld-dev python-dev python-setuptools
pip install MySQL-python
sudo pip install python-jenkins --upgrade
