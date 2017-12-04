arc=/tmp/DGallery_code.tgz

if [ -e $arc ] ; then
  rm -f $arc
fi

cd /home/dymbol/GIT/DGallery/
tar -zcvf /tmp/DGallery_code.tgz .
