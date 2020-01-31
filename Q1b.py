import re, requests, sys
from datetime import datetime
from geolite2 import geolite2

access_log_location = "/home/jacky/access.log"
search_start_time = "2019-06-10 00:00:00 +0800"
search_end_time = "2019-06-19 23:59:59 +0800"
# Seperate to each lines
file_lines = [x.split() for x in open(access_log_location, "r").readlines() if "HTTP" in x]
# Print out the total Number HTTP Requests
print("Total number of HTTP requests: ",len(file_lines))
# Print out the top 10 IP make most requests between the period
records_between_time = [x[0] for x in file_lines if ((datetime.strptime(' '.join([x[3][1:],x[4][:-1]]),"%d/%b/%Y:%H:%M:%S %z") >= datetime.strptime(search_start_time,"%Y-%m-%d %H:%M:%S %z")) and (datetime.strptime(' '.join([x[3][1:],x[4][:-1]]),"%d/%b/%Y:%H:%M:%S %z") <= datetime.strptime(search_end_time,"%Y-%m-%d %H:%M:%S %z")))]
print("Top 10 IP make most requests between ", " ".join([search_start_time, "and", search_end_time]),"\n" + "\n".join(sorted([i for i in set(records_between_time)], key=records_between_time.count,reverse=True)[0:10]))
#Print out the country with most requests originating from
unique_ip = [i for i in list(set([x[0] for x in file_lines]))]
ip_list = [i[0] for i in file_lines]
unique_ip_count = sorted([(i,ip_list.count(i)) for i in unique_ip], key=lambda item:item[1], reverse=True)
countries_json = {}
total_requests = sum([i[1] for i in unique_ip_count])
for i in unique_ip_count:
	x = geolite2.reader().get(i[0])
	if x:
		if 'country' in x:
			try:
				countries_json[x['country']['names']['en']] += i[1]
			except KeyError:
				countries_json[x['country']['names']['en']] = i[1]
		elif 'registered_country' in x:
			try:
				countries_json[x['registered_country']['names']['en']] += i[1]
			except KeyError:
				countries_json[x['registered_country']['names']['en']] = i[1]
	else:
		pass
	total_requests -= i[1]
	try:
		if (sorted(countries_json.items(), key=lambda item:item[1], reverse=True)[0][1] > sorted(countries_json.items(), key=lambda item:item[1], reverse=True)[1][1] + total_requests) and (sorted(countries_json.items(), key=lambda item:item[1], reverse=True)[0][1] > total_requests):
			break
	except IndexError:
		pass
print(sorted(countries_json.items(), key=lambda item:item[1], reverse=True)[0])
