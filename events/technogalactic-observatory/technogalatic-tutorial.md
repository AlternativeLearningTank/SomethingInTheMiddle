## Observing software from the network's gaze

The Observatorium's Raspberry Pi has the sniffing script used in SomethingInTheMiddle
you can directly look into what URLs are being requested through the Etherbox by following these steps:

1. download this javascript client to look into the traffic https://github.com/hivemq/hivemq-mqtt-web-client

2. uncompress the zip file you just downloaded and open the index.html
file in your browser

3. in the "connection" tab enter the following information:
    - host: <IP address of etherbox raspberry pi>
    - port: 9001

4. click in connect and verify that the connection went fine by checking that
the status dot is green

5. in the "subscriptions" tab click on "add new topic to subscription" and enter "sitm/http" as the topic, click subscribe.

6. Sit back, chillax and watch other people's traffic stream through your browser's view.

Have fun!

## Notes for the clinic

1. The *doctor's* computer should be on another network.
2. Autostart `mosquitto` service
3. Auto start sniffer script
