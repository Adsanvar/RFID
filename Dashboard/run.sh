#-!/usr/bin/bash
export FLASK_APP=Dashboard
export FLASK_DEBUG=1
export FLASK_ENV=Development
flask run -h 192.168.1.177 -p 5005
# flask run