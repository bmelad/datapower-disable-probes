# Disable all of your Probes at once...

Using IBM DataPower Gateway, sometimes people tend to forget enabled Probes, which is not recommended and may impact the gateway's performance. This little script scan your gateway (or multiple gateways) to find any enabled Probes and disables them using the REST Management Interface.

## How to use it?

- Make sure you have activated the REST Management Interface on the desired gateways.
- Add each gateway to the end of the script according to the sample.
- **Arguments explanation:**
  - 1st argument: your gateway IP / hostname.
  - 2nd argument: your REST Management Interface listening port.
  - 3rd argument: an administrative username to use.
  - 4th argument: the password of the username.
