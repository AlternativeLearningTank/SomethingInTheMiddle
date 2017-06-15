## Something In The Middle

*Sitm* is a tool that gives artists, designers and educators an easy to use custom WiFi router to work with networks and explore the aspects of our daily communications that are exposed when we use WiFi. Our goal is to encourage open discussions about how we use our devices online.

*Sitm* emerges from our collective practice as the Alternative Learning Tank and is heavily inspired by projects such as [Dowse](http://dowse.equipment/), [alt.exit](http://alternativelearningtank.net/) and the [NetAidKit](https://netaidkit.net/).

*Sitm* is a project initiated by the [*Alternative Learning Tank*](http://alternativelearningtank.net/) and developed during various collective
efforts at Balkoncito in Amsterdam, Constant in Brussels, etc.

## How does it work?

*Sitm* is a specially configured WiFi router that allows you to intercept many of the communications going through it (https is not supported at the moment).

With SiTM you can look into the sites that people are visiting, the headers of what they are reading, the images they are looking at, WiFi networks that they have been connected to before, etc.

*Sitm* is designed with two audiences in mind: as a classroom tool so that students can better understand how their network access works. And as a design kit to enable artists and designers that want to work with networks to focus on their design work rather than going through the arduous technical process of configuring a WiFi router from scratch.

### What will I need?

To create a *sitm* access point you will need:

  - One computer running either OSX or Linux, this can be *your workstation*
  - A Raspberry Pi 3 (RPi from here on)
  - An SD card with a minimum of 8Gb of capacity (we recommend a "Class 10" card with 16Gb)
  - You will need an existing router that connects you to the internet, this will be your *uplink*.
  - And a network cable (CAT5) to connect your Raspberry Pi 3 to the router.

Make sure you have all this stuff available before you get started.

### Burning a Raspbian image to the SD card

#### Configure your Raspbian install

Remember to extend your file system to make full use of the SD card you put in your Rpi and **remember to enable SSH**, in the *Advanced Options* menu of `raspi-config`.

If you don't know how to do this and are already stuck, you can read this guide.

### Connecting the Rpi to your network

#### Finding the IP address of your Rpi

There are many ways of finding the IP address of the Rpi in your network. You will need this IP address many times in the following steps, so write it down and keep it handy.

  1. You can use [Adafruit's Pi Finder](https://github.com/adafruit/Adafruit-Pi-Finder/releases).
  2. you can go to the *sitm* directory in your workstation using a terminal and type:
  ```
  $ source sitm
  $ rpi-find
  ```
  3. you can just type in a terminal:
  ```
  $ arp -na | grep -i b8:27:eb
  ```

### Configuring your RPi for use with *sitm*

SiTM is specifically designed for the Raspberry Pi 3. We have also tested it with success on Raspberry Pi 2 Model B+ using WiFi dongles, but it requires a fair bit of manual tweaking for each different WiFi card, so we recommend you use the Raspberry Pi 3, which comes with a built-in WiFi chip that can work in AP mode making the setup process much less complicated.

### SSH into your Rpi and download SITM

You now have to access your raspberry pi, via ssh:

```
pi@raspberry: $ git clone https://github.com/AlternativeLearningTank/SomethingInTheMiddle.git
pi@raspberry: $ cd SomethingInTheMiddle
```

### Provisioning

Provisioning means installing all the necessary software in your Rpi and leaving it ready to work with the *sitm* tools.

To make *sitm* easy, we wrote a provisioning script for you. You will have to execute this script from the command line, if you have never worked with the terminal you can [follow this tutorial](https://github.com/IDArnhem/CLI-CommandNoir).

```
pi@raspberry: $ cd provision
pi@raspberry: $ sudo ./provision
```

### Side-effects of provisioning

A fresh Rasbian install will have a user account named `pi`, with `raspberry` as default password, this is a so-called *factory setting* that we want to avoid. When the SSH service is enabled this means that anybody can try to log into your Rpi using those default credentials.

During the provisioning process, *sitm* disables the default account and creates another account named `someone`, with `verycurious` as password, but this account will only let you log in using an SSH key pair. *Sitm* does this to try and keep your access point as secure as we can.

### Setting up *password-free* authentication
First we need to make sure we have access to our Rpi, we can use the default
username and password but I like to install an SSH key as well. Follows these steps to get your Rpi to authenticate via SSH.

 1. You can use the `provision/keygen` script to generate an SSH key, this will generate two file in your computer in the `~/.ssh` directory.

 2. Once that key is generated we need to install it in our Rpi, so that it can recognize us when we try to log in. You can execute the `provision/keyinstall` script for that.

 3. Try to SSH into your Rpi by typing `ssh -i id_rpi_default pi@<the_ip_address_of_your_rpi>` and you should be able to log into your Rpi without having to enter a password.


#### Installing *sitm*

You can use the provided script `./sitm-install` to execute the Ansible script that
will install SomethingInTheMiddle and all its associated dependencies.
