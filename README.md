AmI-Lab Basis Integration
================

Install prerequisites:

1. Install pip. Apoi urmatoarele pachete python:
	- pykestrel - client de Kestrel pt. Python
		sudo pip install pykestrel
	- pymongo - client de Mongo pt. Python
	
2. Install kestrel
	Get 2.3.4 from http://robey.github.com/kestrel/download/kestrel-2.3.4.zip
	Unzip into /usr/local/kestrel/kestrel-2.3.4

	Symlink /usr/local/kestrel/kestrel-2.3.4 to /usr/local/kestrel/current
	Goto /usr/local/kestrel/kestrel/scripts/kestrel.sh and modify header to bin/bash instead of bin/sh
	Goto /usr/local/kestrel/kestrel/scripts/kestrel.sh and replace 4096m with 1024m (it requests 8GB of RAM by default !!!cd !!)
	Symlink /usr/local/kestrel/kestrel/scripts/kestrel.sh into /etc/init.d/kestrel
	/etc/init.d/kestrel start
	sudo apt-get install sysv-rc-conf
	run sysv-rc-conf and make kestrel run for runlevels >= 2

	Test that kestrel works:
		# Script 1 - il executam primul pe asta
		import kestrel
		c = kestrel.Connection(['localhost:22133'])
		c.add('test', 'hello there')
		
		# Script 2 - rulat in alt terminal
		import kestrel
		c = kestrel.Connection(['localhost:22133'])
		c.get(‘test’)

3. Install mongo
http://www.ubuntugeek.com/how-to-install-mongodb-on-ubuntu-12-04-precise-server.html
	Dupa parcurgerea pasilor, verificam ca functioneaza Mongo + pyMongo:
		import pymongo
		c = pymongo.Connection()
		db=c.test_db
		db.docs.save({‘ana’: ‘are’, ‘multe’: ‘mere’})

4. Install redis
 	apt-get install redis-server
