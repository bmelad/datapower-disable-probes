import requests, json, base64, sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

verify_ssl = True

def list_domains(base_url, headers):
	return requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()

def list_services(base_url, headers, domain, service_type):
	return requests.get(base_url + 'mgmt/config/' + domain + '/' + service_type, headers = headers, verify = verify_ssl).json()

def disable_service_probe(base_url, headers, domain, service_type, service_name):
	return requests.put(base_url + 'mgmt/config/' + domain + '/' + service_type + '/' + service_name + '/DebugMode', data = json.dumps({ "DebugMode": "off" }), headers = headers, verify = verify_ssl).json()

def disable_probes(datapower_ip, roma_port, username, password):
    base_url = 'https://' + datapower_ip + ':' + str(roma_port) + '/'
    headers = {'Authorization' : 'Basic ' + str(base64.b64encode((username + ':' + password).encode()).decode())}
    enabled_probes = []
    connected = False
    try:
        domains = list_domains(base_url, headers)
        connected = True
    except requests.exceptions.SSLError:
        print('Connection to ' + datapower_ip + ' failed because of a tls trust issue, you may use the -ignore-tls-issues to bypass this.', file=sys.stderr)
    except requests.ConnectionError:
        print('Connection to ' + datapower_ip + ' failed, please verify that the REST Management Interface is enabled.', file=sys.stderr)

    if connected:
        if domains.get('domain'):
            for domain in domains['domain']:
                services_types = [ 'WSGateway', 'MultiProtocolGateway' ]
                for service_type in services_types:
                    services_result = list_services(base_url, headers, domain['name'], service_type)
                    if services_result.get(service_type):
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
            print('Sorry, no enabled Probes were found on ' + datapower_ip + '.')
        else:
            for probe in enabled_probes:
                print('Disabling the Probe for ' + probe['service_type'] + ' \'' + probe['service_name'] + '\' in domain \'' + probe['domain'] + '\'... ')
                r = disable_service_probe(base_url, headers, probe['domain'],  probe['service_type'], probe['service_name'])
                if (r['DebugMode'] == 'Property was updated.'):
                    print(' --> Disabled successfully!')
                else:
                    print(' --> Failed!')

host = ''
port = ''
username = ''
password = ''
usage = "Usage: disable-datapower-probes.py \n\r\t-host <datapower-hostname> \n\r\t-port <dataport-roma-interface-port> \n\r\t-username <datapower-administrative-username> \n\r\t-password <password-of-the-administrative-user> \n\r\t-ignore-tls-issues <true|false> (optional, default is false)"

i = 1
while i < len(sys.argv):
    if (sys.argv[i] == '-host'):
        i += 1
        if i < len(sys.argv):
            host = sys.argv[i]
    elif (sys.argv[i] == '-port'):
        i += 1
        if i < len(sys.argv):
            port = sys.argv[i]
    elif (sys.argv[i] == '-username'):
        i += 1
        if i < len(sys.argv):
            username = sys.argv[i]
    elif (sys.argv[i] == '-password'):
        i += 1
        if i < len(sys.argv):
            password = sys.argv[i]
    elif (sys.argv[i] == '-ignore-tls-issues'):
        i += 1
        if i < len(sys.argv):
            if sys.argv[i].lower() != 'true' and sys.argv[i].lower() != 'false':
                print('Illegal value for -ignore-tls-issues argument.')
                verify_ssl = ''
            elif sys.argv[i].lower() == 'true':
                verify_ssl = False
            else:
                verify_ssl = True
    i += 1
    
if host == '' or port == '' or username == '' or password == '' or verify_ssl == '':
    print(usage, file=sys.stderr)
    sys.exit(2)

disable_probes(host, port, username, password)

