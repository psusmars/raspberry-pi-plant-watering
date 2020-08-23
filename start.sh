source water/bin/activate
gunicorn --workers 5 --bind unix:simpleapp.sock -m 007 /home/pi/raspberry-pi-plan-water:app
deactivate