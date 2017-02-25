## OpenAPS share 
Repository to share various work related to OpenAPS.

### Temporary targets
The current solution for setup temporary targets is to set them from nightscout. For this it is necessary to have internet connection, which is not always possible and sometimes problematic.

#### Shell script
start-temp-target.sh - script able to change temporary target in settings/temptarget.json, to be able to use it, nightscout download of temptargets needs to be disabled.

The script can be used from [Hot Button application](https://play.google.com/store/apps/details?id=crosien.HotButton).

TODO: rewrite in more json friendly way e.g. Node.js, improve parameter handling, ...

#### Web service 
##### Installation
- clone this repository
- install dependencies: ```sudo pip install flask```
- to start the service: ```OPENAPSROOT=/path/to/youropenaps APSapi.py```
- to run on startup add to the crontab: ```@reboot OPENAPSROOT=/path/to/your/openaps /path/to/service/APSapi.py```

The service uses by default port 5001.

##### Android
[Http Request Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts) can be used to create various buttons for Http requests. 

<img src="https://github.com/lukas-ondriga/openaps-share/blob/master/Screenshot_20170218-162143.png" alt="Http Shortcuts 1" width="250"/>
<img src="https://github.com/lukas-ondriga/openaps-share/blob/master/Screenshot_20170218-162223.png" alt="Http Shortcuts 2" width="250"/>

##### Pebble
[Http Push](https://apps.getpebble.com/en_US/application/567af43af66b129c7200002b) is pebble application where you can create custom http buttons. No registration anywhere is required and you do not need an internet connection to execute your requests.

<img src="https://github.com/lukas-ondriga/openaps-share/blob/master/Screenshot_20170218-162111.png" alt="Pebble" width="250"/>
