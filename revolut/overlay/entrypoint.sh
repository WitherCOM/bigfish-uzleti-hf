gunicorn --workers 2 --bind unix:/var/run/app.sock -m 777 main:app -k uvicorn.workers.UvicornWorker > /dev/stdout &
exec nginx -g 'daemon off;';
