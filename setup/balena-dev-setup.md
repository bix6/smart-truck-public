# Balena Dev Setup
		
## Follow this (I used Python, if the link is still down you can find the info on Github)				
- https://www.balena.io/docs/learn/getting-started/raspberrypi3/nodejs/				
- https://github.com/balena-io-projects/simple-server-python				
				
## Check remotes				
- git remote -v				
- remove remotes as needed				
- git remote rm name				
- Add remote (copy link from dashboard)				
				
## Install CLI				
- https://www.balena.io/docs/reference/cli/#local-configure-target-				
- https://github.com/balena-io/balena-cli				
- NPM install didn't work for me so I used the standalone install				
- Download and unzip the OS				
- https://github.com/balena-io/balena-cli/releases				
- Copy balena-cli folder into /usr/local/lib			
- cp -R ~/Desktop/balena-cli /usr/local/lib				
- Add folder to path				
- sudo nano /etc/paths				
- add: /usr/local/lib/balena-cli				
- Open new terminal and type balena to confirm				
- Future updates: download new balena file and move it into lib				
- rm -Ri /usr/local/lib/balena-cli				
- cp -R ~/Desktop/balena-cli /usr/local/lib				
				
- Turn on local mode for each device under actions				
## Login				
- balena login				
- web authentication				
- Find devices				
- sudo balena local scan				
- Reboot device from console				
				
- Sudo balena local push #####.local -s .				
				
- sudo balena local ssh #####.local				
- sudo balena local ssh #####.local —host 				
- exit				
				
- balena preload balena-beta.img --beta				