Q2:
Need to have credentials files with the access key and secret
```
~/.aws/credentials

[default]
aws_access_key_id = {KEY}
aws_secret_access_key = {SECRET}

```
And config file with the region
```
~/.aws/config

[default]
region={REGION}

```
Also you need to config ssh_folder in the Q2.py script to your ssh directory with all the ssh keys.

