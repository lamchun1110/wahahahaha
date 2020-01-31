import boto3, sys, os

def check_name_tag(name_tag):
	region = 'ap-southeast-1'
	ssh_folder = "/home/jacky/.ssh/"
	ec2 = boto3.resource('ec2',region)
	client = boto3.client('ec2-instance-connect')
	# Get information for all running instances
	running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
	# Find the instances which match the name tag
	match_name_tag_instances = [(instance.id,instance.public_ip_address,instance.placement['AvailabilityZone'],instance.key_name) for instance in running_instances for tag in instance.tags if (('Name'in tag['Key']) and (tag['Value'] == name_tag))] 
	if len(match_name_tag_instances) == 1:
		#Execute the SSH command
		os.execl("/usr/bin/ssh","ssh","-l", "ec2-user", match_name_tag_instances[0][1], "-i", ssh_folder + match_name_tag_instances[0][3])
	elif len(match_name_tag_instances) > 1:
		print("More than one server with this name tag")
	else:
		print("Host not found")
if __name__ == '__main__':
	check_name_tag(sys.argv[1])