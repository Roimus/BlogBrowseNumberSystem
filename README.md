先初始化数据python manage.py makemigrations  python manage.py migrate
然后初始化命令 python manage.py create_articles 添加文章表数据
先开redis然后开celery  celery -A BlogBrowseNumberSystem worker -l info
最后开始服务 python manage.py runserver
在postman中导入项目中postman文件夹下的接口文档。直接使用就行
