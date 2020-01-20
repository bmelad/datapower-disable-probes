# Disable all of your Probes at once...

Using IBM DataPower Gateway, sometimes people tend to forget enabled Probes, which is not recommended and may impact the gateway's performance. This little script scan your gateway (or multiple gateways) to find any enabled Probes and disables them using the REST Management Interface.

## How to use it?

- Make sure you have activated the REST Management Interface on the desired gateways.

- **Arguments explanation:**
  - host: your gateway IP / hostname.
  - port: your REST Management Interface listening port.
  - username: an administrative username to use.
  - password: the password of the username.
  - ignore-tls-issues: should the script ignore ssl/tls issues (true or false)?
