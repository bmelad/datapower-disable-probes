import requests, json, base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def list_domains(base_url, headers):
	return requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = False).json()

def list_services(base_url, headers, domain, service_type):
	return requests.get(base_url + 'mgmt/config/' + domain + '/' + service_type, headers = headers, verify = False).json()

def disable_service_probe(base_url, headers, domain, service_type, service_name):
	return requests.put(base_url + 'mgmt/config/' + domain + '/' + service_type + '/' + service_name + '/DebugMode', data = json.dumps({ "DebugMode": "off" }), headers = headers, verify = False).json()

def disable_probes(datapower_ip, roma_port, username, password):
	base_url = 'https://' + datapower_ip + ':' + str(roma_port) + '/'
	headers = {'Authorization' : 'Basic ' + base64.b64encode(username + ':' + password)}
	enabled_probes = []
	domains = list_domains(base_url, headers)
	if domains.has_key('domain'):
		for domain in domains['domain']:
			services_types = [ 'WSGateway', 'MultiProtocolGateway' ]
			for service_type in services_types:
				services_result = list_services(base_url, headers, domain['name'], service_type)
				if service_type in services_result:
					if (isinstance(services_result[service_type], list)):					
						for service in services_result[service_type]:
							#print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
							if service['DebugMode'] == 'on':
								enabled_probes.append({ 'domain': domain['name'] , 'service_type': service_type, 'service_name': service['name'] })
								
					else:
						service = services_result[service_type]
						#print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
						if service['DebugMode'] == 'on':
							enabled_probes.append({ 'domain': domain['name'], 'service_type': service_type, 'service_name': service['name'] })
	if not enabled_probes:
		print("No enabled Probes were found.")
	else:
		for probe in enabled_probes:
			print('Disabling the Probe for ' + probe['service_type'] + ' \'' + probe['service_name'] + '\' in domain \'' + probe['domain'] + '\'... ')
			r = disable_service_probe(base_url, headers, probe['domain'],  probe['service_type'], probe['service_name'])
			if (r['DebugMode'] == 'Property was updated.'):
				print(' --> Disabled successfully!')
			else:
				print(' --> Failed!')

# 1st argument: your gateway IP / hostname.
# 2nd argument: your REST Management Interface listening port.
# 3rd argument: an administrative username to use.
# 4th argument: the password of the username.
disable_probes('your-gateway-address', 5554, 'username', 'password')
