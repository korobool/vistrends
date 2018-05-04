start:
	supervisord -c supervisord.conf
stop:
	supervisorctl -c supervisord.conf shutdown
ctl:
	supervisorctl -c supervisord.conf
