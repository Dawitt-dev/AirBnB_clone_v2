#!/usr/bin/env bash
# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
printf %s "
events {
	 worker_connections 768;
}
https {
	server {
		listen 80 default_server;
		listen [::]:80 default_server;
		add_header X-Served-By $HOSTNAME;
		root   /var/www/html;
		index  index.html index.htm;

		location /hbnb_static {
			alias /data/web_static/current/;
			index index.html index.htm;
		}
		location /redirect_me {
			return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
		}

		error_page 404 /404.html;
		location /404 {
			root /var/www/html;
			internal;
		}
	}
}" > /etc/nginx/nginx.conf

# Restart Nginx
sudo service nginx restart

exit 0
