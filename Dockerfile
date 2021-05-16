FROM nginx:latest

COPY frontend/dist /app
COPY nginx.conf /etc/nginx/conf.d/default.conf
