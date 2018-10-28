To set up:  
git clone https://github.com/kx499/ThrIndicator.git   
virtualenv ThrIndicator  
cd ThrIndicator  
bin/pip install -r requirements.txt  
./db_create.py

To run GUI/Webserver:
./run.py  
Note: if not running on localhost, add host=0.0.0.0 to app.run() in run.py, or use ./run.py --prod

To run feeds, this is meant to be run with cron - I opted not to use celery. It was overkill. 
./pull_feeds.py

See config.py for feed configuration examples

On Debian or Ubuntu systems, you will need to `sudo apt install git python-virtualenv python-pip python-dev`