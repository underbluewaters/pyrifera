import boto.ec2
import datetime
AWS_ACCESS_KEY = 'access-key-here'
AWS_SECRET_KEY = 'secret-key-here'
VOLUME_ID = 'vol-id-here'

conn = boto.ec2.connect_to_region("us-west-2",
	aws_access_key_id=AWS_ACCESS_KEY,
	aws_secret_access_key=AWS_SECRET_KEY)

today = datetime.date.today()
name = VOLUME_ID + ' Backup - ' + str(today)
snapshot = conn.create_snapshot(VOLUME_ID, name)
print 'Made snapshot named "' + name + '"'
