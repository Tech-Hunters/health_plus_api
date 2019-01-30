import os

from api import app

if __name__ == "__main__":
    app.debug = True
    #app.config['DATABASE_NAME'] = 'test'
    #host = os.environ.get('IP', '0,0,0,0')
    #port = int(os.environ.get('PORT', '8080'))
    app.run(host='0.0.0.0', port=8080)
    
