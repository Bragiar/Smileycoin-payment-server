## SMILEYCOIN PAYMENT SERVER
This is a smileycoin payment server that sends out payment links to the HTML5 wallet (wallet.smileyco.in) and tracks the payments

# About
this is a simple Flask server that uses two api calls
either `/getpaymentlink`, which returns:
```json
{
  "address": "B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ",
  "amount": 20,
  "link": "https://wallet.smileyco.in/?network=smileycoin&address=B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ&amount=20",
  "message": ""
}
```
amount refers to amount to be paid in smileycoin.

and `/verifypayment/<address>` returns:

```json
{
  "amount": 0,
  "confirmations": 0,
  "paid": "no",
  "unconfirmed": "no"
}
```
or if it is paid:
```json
{
  "amount": 20.0,
  "confirmations": 0,
  "paid": "yes"
}
```


## How to run
1. Start by compiling your smileycoin wallet. Instructions can be found here for Unix: (https://github.com/smileycoin/smileyCoin/blob/master/doc/build-unix.md) and start the smileycoin wallet
2. Clone this repository

3. Install Python
```
sudo apt-get update # Update your local packages
```
And
```
sudo apt-get install python3-pip python3-dev # install dependencies
```
4. Create a venv in the project repository
Venv is a package comes with Python3. i.e you need not to install venv separately. It serves a similar purpose to virtualenv, and works in a very similar way, but it doesn't need to copy Python binaries around (except on Windows). Though vitualenv is more popular here I’m using venv just for familiarity. To create a venv use below command:
```
python3 -m venv <your venv>
Note: Venv is only for python3 for python2 you should use virtualenv
```
Or create a virtualenv

virtualenv is a very popular tool that creates isolated Python environments for Python libraries.
Install Virtualenv in python2:
```
sudo pip install virtualenv
```
Install Virtualenv in python3:
```
sudo pip3 install virtualenv
```
Create Virtualenv:
```
virtualenv <your virtualenv>
```
Activate virtualenv:
```
source yourvirtualenv/bin/activate

Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this
(yourvirtualenv)user@host:~/src$.
```

5. Install flask

```
pip install flask
```
6. Configure your server
Go into the config.py file and make sure the path to smileycoind is correct and make sure the wallet is up and running
Also you can set the amount to be paid in smileycoins there
7. Test your Flask app by typing:
```
curl 'http://localhost:5000/getpaymentlink'

```
and you should get something like

```json
{
  "address": "B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ",
  "amount": 20,
  "link": "https://wallet.smileyco.in/?network=smileycoin&address=B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ&amount=20",
  "message": ""
}
```
## Deploy to production using Gunicorn and Nginx

1. Install nginx
```
sudo apt-get install nginx
```
2. In the virtual environment install Gunicorn
```
pip install gunicorn flask
```
3. Create a WSGI entry point
Next, we’ll create a file that will serve as the entry point for our application. This will tell our Gunicorn server how to interact with the application.
```
nano ~/smileycoin-payment-server/wsgi.py
```
we can simply import the Flask instance from our application and then run it:
```
from app import app

if __name__ == "__main__":
    app.run()
```

*Folder structure*

```
smileycoin-payment-server
  |____ app.py
  |____ wsgi.py
  |____ myprojectvenv
```

4. Test the Gunicorn availability to serve the application:
Now test the ability of Gunicorn to serve the project. We can do it by the name of the module (except .py extension) plus the name of the callable within the application (i.e ) wsgi:app. We’ll also specify the interface and port to bind to so that it will be started on a publicly available interface:
```
cd ~/smileycoin-payment-server
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Now run the following command
```
curl 'http://localhost:5000/getpaymentlink'

```
and you should get something like

```json
{
  "address": "B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ",
  "amount": 20,
  "link": "https://wallet.smileyco.in/?network=smileycoin&address=B9wFPjkMknQ3aoVdbJjhhXeXoFBjUCdnAJ&amount=20",
  "message": ""
}
```

Now deactivate virtualenv by following command:

```
deactivate
```

5. Create a systemd UNIT file
systemd unit file will allow Ubuntu’s init system to automatically start Gunicorn and serve our Flask application whenever the server boots.
Create a unit file ending in .service within the /etc/systemd/system directory to begin :

```
sudo nano /etc/systemd/system/app.service
```

```
[Unit]
#  specifies metadata and dependencies
Description=Gunicorn instance to serve myproject
After=network.target
# tells the init system to only start this after the networking target has been reached
# We will give our regular user account ownership of the process since it owns all of the relevant files
[Service]
# Service specify the user and group under which our process will run.
User=yourusername
# give group ownership to the www-data group so that Nginx can communicate easily with the Gunicorn processes.
Group=www-data
# We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
WorkingDirectory=/home/bra26/work/deployment/smileycoin-payment-server
Environment="PATH=/home/bra26/work/deployment/smileycoin-payment-server/myprojectvenv/bin"
# We'll then specify the commanded to start the service
ExecStart=/home/bra26/work/deployment/smileycoin-payment-server/myprojectvenv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app
# This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running:
[Install]
WantedBy=multi-user.target
```

Note: In the last line of [Service] We tell it to start 3 worker processes. We will also tell it to create and bind to a Unix socket file within our project directory called app.sock. We’ll set a umask value of 007 so that the socket file is created giving access to the owner and group, while restricting other access. Finally, we need to pass in the WSGI entry point file name and the Python callable within.


We can now start the Gunicorn service we created and enable it so that it starts at boot:



```
sudo systemctl start app
sudo systemctl enable app
```

*Folder structure*

A new file app.sock will be created in the project directory automatically.


```
src
  |____ app.py
  |____ wsgi.py
  |____ myprojectvenv
  |____ app.sock
```

6. Final step: configuring nginx
Gunicorn application server is now be up and running and it waits for requests on the socket file in the project directory. We need to configure Nginx to pass web requests to that socket by making some small additions to its configuration file.
We’ll need to tell NGINX about our app and how to serve it.
cd into /etc/nginx/. This is where the NGINX configuration files are located.
The two directories we will work on are sites-available and sites-enabled.
* sites-available contains individual configuration files for all of your possible static app.
* sites-enabled contains links to the configuration files that NGINX will actually read and run.
create a new server block configuration file in Nginx’s sites-available directory named app

```
sudo nano /etc/nginx/sites-available/app
```

Open up a server block and tell Nginx to listen on the default port 80. We also need to tell it to use this block for requests for our server’s domain name or IP address:

```
server {
    listen 80;
    server_name server_domain_or_IP;
}
```

another thing that we need to add is a location block that matches every request. Within this block, we’ll include the proxy_paramsfile that specifies some general proxying parameters that need to be set. We’ll then pass the requests to the socket we defined using the proxy_passdirective:
```
server {
    listen 80;
    server_name server_domain_or_IP;

location / {
  include proxy_params;
  proxy_pass http://unix:/home/bra26/work/deployment/smilecoin-payment-server/app.sock;
    }
}
```

*Enable Nginx server block*
To enable the Nginx server block configuration we’ve just created, link the file to the sites-enabled directory. The syntax is as follows:

```
ln -s <SOURCE_FILE> <DESTINATION_FILE>
```

The actual syntax will look like:
```
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
```
Note: With the file in that directory, we can test for syntax errors by typing: `sudo nginx -t` If this does not indicate any issues, we can restart the Nginx process to read our new config:

```
sudo systemctl restart nginx
```

The last thing we need to do is adjust our firewall to allow access to the Nginx server:

```
sudo ufw allow 'Nginx Full'
```
You should now be able to go to your server’s domain name or IP address in your web browser and see your app running.

```
http://server_domain_or_IP
```

Your deployment is done!
