#required module

I) pip install bcrypt
II) pip install djangorestframework

III) sudo apt-get install libmysqlclient-dev
 or in case of mariadb
III) sudo apt-get install libmariadbclient-dev

IV) pip install mysqlclient


apart from this manage separate install of mysql/mariadb or remote mysql and configuration will be as follow  in QtoChat/QtoChat/setting.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qtochat',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': ''
    }
}





mySQLdb is a python interface for mysql, but it is not mysql itself. And apparently mySQLdb needs the command 'mysql_config', so you need to install that first.

Can you confirm that you did or did not install mysql itself, by running "mysql" from the shell? That should give you a response other than "mysql: command not found".

Which linux distribution are you using? Mysql is pre-packaged for most linux distributions. For example, for debian / ubuntu, installing mysql is as easy as

sudo apt-get install mysql

mysql-config is in a different package, which can be installed from (again, assuming debian / ubuntu):

sudo apt-get install libmysqlclient-dev

if you are using mariadb, the drop in replacement for mysql, then run

sudo apt-get install libmariadbclient-dev

pip install mysqlclient
