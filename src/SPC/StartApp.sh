APP_DIR=/opt/BDG/DymbolGallery
IP=192.168.122.124
WSGI_FILE=DymbolGallery.wsgi
LOG=/opt/GoPG_conf/bdg.log
STATIC_DIR=/opt/GoPG/DymbolGallery/photos/static
PID_FILE=/opt/GoPG_conf/bdg.pid

uwsgi --http $IP:8000 --chdir $APP_DIR  --wsgi-file $WSGI_FILE --master --processes 1 --workers 1 --threads 1 --daemonize=$LOG  --static-map /static=$STATIC_DIR --pidfile $PID_FILE
