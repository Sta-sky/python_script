# django + uwsgi + nginx 使用docker部署

### 一、创建django项目，创建一个简单app用于测试，

### 二、创建uwsgi目录
    1、创建uwsgi.ini 文件
        [uwsgi]
        # 配置服务器的监听ip和端口，让uWSGI作为nginx的支持服务器的话，设置socket就行；
        socket = :101  (此处不写ip表示主机的内网外ip都可访达)

        # 配置项目目录（此处设置为项目的根目录,用docker部署的话，为映射到docker中的根目录）
        chdir = /service

        # 配置入口模块 (django的入口函数的模块，即setting同级目录下的wsgi.py)
        module = docker_server.wsgi
         
        # 开启master, 将会多开一个管理进程, 管理其他服务进程
        master = True
         
        # 监听队伍最大长度，默认128
        listen=128
         
        # 服务器开启的进程数量
        processes = 4
         
        # 以守护进程方式提供服, 输出信息将会打印到log中
        daemonize = /service/uwsgi/uwsgi.log
         
        # 服务器进程开启的线程数量
        threads = 4
         
        # 退出的时候清空环境变量
        vacuum = true
        
        # 进程pid
        pidfile = /service/uwsgi/uwsgi.pid
         
        #修改python代码时，自动重启uwsgi服务
        #py-autoreload = 1
    2、创建uwsgi.log uwsgi.pid 

### 三、创建配置nginx，让nginx接收的请求，通过socket发送到uwsgi

    server {
        listen 70; # nginx监听端口
        server_name docker_django; 
        location / {
            # 此处为nginx自带的uwsgi_params路径
            include /etc/nginx/uwsgi_params; 

            # 发送到uwsgi的 ip：port，如果是docker，则查看uwsgi的docker服务的ip，查看命令：
                docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' django_uwsgi
            uwsgi_pass 172.18.0.3:101;  
        }
        location /static {
            alias /service/static;  #静态文件地址
        }
    }

### 四、创建dockerfile、docker-compose.yml 
    注：
        参见本项目dockerfile，docker-compose

        dockerfile中最后执行 CMD时，由于docker必须有一个前台进程运行，
        所以在CMD后面加 tail /dev/null  保证dockr不一直处于starting状态中
            
            CMD uwsgi --ini /service/uwsgi/uwsgi.ini && tail -f /dev/null 





        

    

    

    
        