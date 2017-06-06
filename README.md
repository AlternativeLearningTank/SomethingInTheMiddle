## Something In The Middle

*Sitm* is a tool that gives artists, designers and educators an easy to use custom WiFi router to work with networks and explore the aspects of our daily communications that are exposed when we use WiFi. Our goal is to encourage open discussions about how we use our devices online.

*Sitm* emerges from our collective practice as the Alternative Learning Tank and is heavily inspired by projects such as [Dowse](http://dowse.equipment/), [alt.exit](http://alternativelearningtank.net/) and the [NetAidKit](https://netaidkit.net/).


## How does it work?

*Sitm* is a specially configured WiFi router that allows you to intercept all the communications going through it. With SiTM you can look into the sites that people are visiting, the headers of what they are reading, the images they are looking at, etc.

*Sitm* is designed with two audiences in mind: as a classroom tool so that students can better understand how their network access works. And as a design kit to enable artists and designers that want to work with networks to focus on their design work rather than going through the arduous technical process of setting up a router from scratch.

### Setting up your RPi for the first time

SiTM is specifically designed for the Raspberry Pi 3. We have also tested it with success on Raspberry Pi 2 Model B+ using WiFi dongles, but it requires a fair bit of manual tweaking for each different WiFi card, so we recommend you use the Raspberry Pi 3, which comes with a built-in WiFi chip that can work in AP mode.

### Provisioning

Provisioning means installing all the necessary software in your Rpi and leaving it ready to work with the *sitm* tools.

To make *sitm* easy, we decided to use an automated provisioning tool, instead of giving you step by step instructions as it simply would be too long and intimidating a process.

You will need to have the provisioning tool installed in your computer before you can start. It is called [*Ansible*](https://www.ansible.com/) and you install it like this:

##### On OSX

Assuming you have [Homebrew](http://brew.sh/) installed:
```
brew install ansible
```

##### On Linux
```
apt-get install ansible
```

#### Setting up authentication
First we need to make sure we have access to our Rpi, we can use the default
username and password but I like to install an SSH key as well. Follows these steps to get your Rpi to authenticate via SSH.

 1. You can use the `provision/keygen` script to generate an SSH key, this will generate two file in your computer in the `~/.ssh` directory.

 2. Once that key is generated we need to install it in our Rpi, so that it can recognize us when we try to log in. You can execute the `provision/keyinstall` script for that.

 3. Try to SSH into your Rpi by typing `ssh -i id_rpi_default pi@<the_ip_address_of_your_rpi>` and you should be able to log into your Rpi without having to enter a password.

If you do not know how to get the IP address of your Rpi, you can use [Adafruit's Pi Finder](https://github.com/adafruit/Adafruit-Pi-Finder/releases).

#### Installing *sitm*

You can use the provided script `./sitm-install` to execute the Ansible script that
will install SomethingInTheMiddle and all its associated dependencies.

#### Installing everything you'll need

To install everything you will need you can use the Ansible script we provide you with, like this:

```
ansible-playbook -c paramiko -i ansible/hosts ansible/main.yml --sudo
```
