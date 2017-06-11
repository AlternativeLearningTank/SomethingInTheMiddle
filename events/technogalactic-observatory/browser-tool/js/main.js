var sitmclient = {
    'client': null,
    'lastMessageId': 1,
    'lastSubId': 1,
    'subscriptions': [],
    'messages': [],
    'observing': false,

    'init' : function() {
      console.log("sitm::init");
    },

    'connect': function () {
        this.client = new Messaging.Client(wsbroker, wsport, "galactiquebrowser_" + parseInt(Math.random() * 100, 10));
        this.client.onConnectionLost = this.onConnectionLost;
        this.client.onMessageArrived = this.onMessageArrived;

        var options = {
          timeout: 3,
          onSuccess: this.onConnected,
          onFailure: this.onFailedConnection
        };

        this.client.connect( options );
    }, // connect

    'onConnected': function() {
      console.log("connected to sitm");
      console.log("subscribing to " + mqtt_topic);
      sitmclient.client.subscribe(mqtt_topic, {qos: 0});
      sitmclient.observing = true;
      $('div#log').empty();
      $('a#btnStart').html('Stop observation');
      $('a#btnStart').toggleClass("alert");
    },

    'onFailedConnection': function() {
      console.log("Connection failed: " + message.errorMessage);
      sitmclient.observing = false;
    },

    'start': function() {
      console.log("Stating observation");
      this.connect();
    },

    'stop': function() {
      console.log("Stopping observation");
      this.client.disconnect();
      this.observing = false;
      $('a#btnStart').html('Start observation');
      $('a#btnStart').toggleClass("alert");
    },

    'toggle': function() {
      if(this.observing) {
        this.stop();
      } else {
        this.start();
      }
    }, // toggle

    'onConnectionLost': function (responseObject) {
      console.log("connection lost: " + responseObject.errorMessage);
    },

    'onMessageArrived': function (message) {
      console.log("<< " + message.payloadString);
      $('div#log').append(message.payloadString + '<br/>');
    },
};
