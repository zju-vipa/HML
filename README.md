# HML
Human in the loop Machine Learning System



## Installation

Install docker images

- hml
- hml-sql
- hml-web



### hml image

1、download docker image

```bash
docker pull nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

docker run -itd --name=hml --gpus all nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
```



2、install the dependencies

```bash
apt-get update
apt-get install vim openssh-server nginx supervisor redis-server screen -y
```



3、install python

```bash
wget -c https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh

bash Anaconda3-2019.10-Linux-x86_64.sh

pip install numpy pandas scipy matplotlib jupyter scikit-learn torch torchvision pymysql flask_sqlalchemy flask flask-cors gunicorn gevent celery redis --timeout 60000000
```



4、use nginx

- nginx.conf

```
vim /etc/nginx/nginx.conf

user www-data;
# lsy_change
worker_processes auto;
# worker_processes 4;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        # lsy_change
        # keepalive_timeout 65;
        keepalive_timeout 300;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;
        
        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
```

- hml.conf

```
server {
    listen 0.0.0.0:8021;

    location / {
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

        if ($request_method = 'OPTIONS') {
            return 204;
        }

        proxy_pass http://127.0.0.1:8025;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_redirect off;
        proxy_set_header Host $host:8021;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_send_timeout 300;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
}
```



5、use redis

```
vim /etc/redis/redis.conf

################################# GENERAL #####################################

# By default Redis does not run as a daemon. Use 'yes' if you need it.
# Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
# lsy_change
# daemonize yes
daemonize no
```



6、use supervisor

- supervisord.conf

```
vim /etc/supervisor/supervisord.conf

; supervisor config file
  
;[unix_http_server]
;file=/var/run/supervisor.sock   ; (the path to the socket file)
;chmod=0700                      ; sockef file mode (default 0700)

[inet_http_server]         ; inet (TCP) server disabled by default
port=0.0.0.0:8020          ; (ip_address:port specifier, *:port for all iface)
username=lsy               ; (default is no username (open server))
password=lsy               ; (default is no password (open server))

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
;serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=http://0.0.0.0:8020  ; use an http:// url to specify an inet socket
username=******                   ; should be same as http_username if set
password=******                   ; should be same as http_password if set

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf
```

- hml.conf

```
vim /etc/supervisor/conf.d/hml.conf

[program:HML]
command=/root/anaconda3/envs/hml/bin/gunicorn -c config_gunicorn.py wsgi:app
directory=/root/HML
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_gunicorn_stdout.log
stderr_logfile=/root/HML/log/supervisor_gunicorn_stderr.log
```

- hml_nginx.conf

```
vim /etc/supervisor/conf.d/hml_nginx.conf

[program:nginx]
command=/usr/sbin/nginx -g 'daemon off;'
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_nginx_stdout.log
stderr_logfile=/root/HML/log/supervisor_nginx_stderr.log
```

- hml_flower.conf

```
vim /etc/supervisor/conf.d/hml_flower.conf

[program:flower]
command=/root/anaconda3/envs/hml/bin/flower -A celery_tasks --address=0.0.0.0 --port=8022 --broker=redis://127.0.0.1:6379/0
directory=/root/HML
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_flower_stdout.log
stderr_logfile=/root/HML/log/supervisor_flower_stderr.log
```

- hml_redis.conf

```
vim /etc/supervisor/conf.d/hml_redis.conf

[program:redis]
command=/usr/bin/redis-server
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_redis_stdout.log
stderr_logfile=/root/HML/log/supervisor_redis_stderr.log
```

- hml_celery1.conf

```
vim /etc/supervisor/conf.d/hml_celery1.conf

[program:celery1]
command=/root/anaconda3/envs/hml/bin/celery -A celery_tasks worker --loglevel=INFO --concurrency=8 --hostname=worker1@%%h
directory=/root/HML
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_celery1_stdout.log
stderr_logfile=/root/HML/log/supervisor_celery1_stderr.log
```

- hml_celery2.conf

```
vim /etc/supervisor/conf.d/hml_celery2.conf

[program:celery2]
command=/root/anaconda3/envs/hml/bin/celery -A celery_tasks worker --loglevel=INFO --concurrency=8 --hostname=worker2@%%h
directory=/root/HML
startsecs=0
stopwaitsecs=0
autostart=false
autorestart=true
stdout_logfile=/root/HML/log/supervisor_celery2_stdout.log
stderr_logfile=/root/HML/log/supervisor_celery2_stderr.log
```



7、start supervisord

```bash
supervisord -c /etc/supervisor/supervisord.conf
supervisorctl reload

# program_name is the "x" of "[program:x]"
supervisorctl start program_name
supervisorctl stop program_name
supervisorctl restart program_name
```



8、start nginx (you also can use supervisord to start nginx)

```bash
nginx -c /etc/nginx/nginx.conf
nginx -s reload
nginx -s quit
```



9、when you need to kill the processes

```bash
ps -A | grep supervisord 
kill -9 $(pgrep supervisord)

ps -A | grep nginx 
kill -9 $(pgrep nginx)
```



10、commit change

```bash
docker commit -m "hml backend environment" -a "lsy" 60db6386e2ba lsy/hml:1.0.4

docker run -p 8020:8020 -p 8021:8021 -p 8022:8022 -v /disk2/lsy/HML:/root/HML -v /etc/localtime:/etc/localtime -itd --name=hml --gpus all lsy/hml:1.0.4
```



### hml-mysql image

1、download docker image

```bash
docker pull mysql:8.0.19

docker volume create hml-mysql

docker container run -p 8023:3306 --mount source=hml-mysql,destination=/var/lib/mysql -v /etc/localtime:/etc/localtime -e MYSQL_ROOT_PASSWORD=****** --name hml-mysql -d mysql:8.0.19
```



2、create database

```bash
docker container exec -it hml-mysql bash

mysql -u****** -p******

CREATE USER '******'@'%' IDENTIFIED WITH mysql_native_password BY '******';

GRANT ALL PRIVILEGES ON *.* TO '******'@'%';

flush privileges;
```



3、commit change

```bash
docker stop hml-mysql

docker commit -m "mysql environment" -a "lsy" 6dc704b01986 lsy/hml-mysql:1.0.0

docker container run -p 8023:3306 --mount source=hml-mysql,destination=/var/lib/mysql -v /etc/localtime:/etc/localtime -e MYSQL_ROOT_PASSWORD=hml --name hml-mysql -d lsy/hml-mysql:1.0.0
```



### hml-web image

1、download docker image

```bash
docker pull nginx:1.18.0

docker run -p 8030:8030 -v /etc/localtime:/etc/localtime -v /disk2/lsy/HML-WEB:/usr/share/nginx/html -d --name hml-web nginx:1.18.0
```



2、edit nginx config

```bash
docker exec -it hml-web bash

vim /etc/nginx/conf.d/hml-web.conf
```

with

```
server {
    listen 0.0.0.0:8030;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html; 
    }

    location /user {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
    location /dataset {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
    location /algorithm {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
    location /featureEng {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
    location /learner {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
    location /decision {
        proxy_pass http://10.214.211.205:8021/api/private/v1$request_uri;
    }
}
```



3、commit change

```bash
docker stop hml-web

docker commit -m "hml web environment" -a "lsy" 60db6386e2ba lsy/hml-web:1.0.0

docker run -p 8030:8030 -v /etc/localtime:/etc/localtime -v /disk2/lsy/HML-WEB:/usr/share/nginx/html -d --name hml-web lsy/hml-web:1.0.0
```

