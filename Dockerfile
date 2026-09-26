FROM nginx:1.27-alpine

COPY index.html manifest.webmanifest sw.js .nojekyll /usr/share/nginx/html/
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY data /usr/share/nginx/html/data
COPY icons /usr/share/nginx/html/icons

EXPOSE 80
