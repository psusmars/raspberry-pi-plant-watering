server {
 
    server_name simpleapp.techcoil.com;
    listen 80;
    root /var/flaskapp/water/static;
 
    location / {
        try_files $uri @water-flask;
    }
 
    location @water-flask {
        include proxy_params;
        proxy_pass http://unix:/var/flaskapp/water/water.sock;
    }
 
}