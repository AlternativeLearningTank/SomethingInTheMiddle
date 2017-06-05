# -*- mode: ruby -*-
# vi: set ft=ruby :

# IP Address for the host only network, change it to anything you like
# but please keep it within the IPv4 private network range
sitm_devbox_ip = "172.22.22.22"

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.box = "ARTACK/debian-jessie"

	# Use hostonly network with a static IP Address and enable
	# hostmanager so we can have a custom domain for the server
	# by modifying the host machines hosts file
	config.hostmanager.enabled = true
	config.hostmanager.manage_host = true

	config.ssh.forward_agent = true

	config.vm.define "sitm" do |uman|
		uman.vm.hostname = "sitm.local"
		uman.vm.network :private_network, ip: sitm_devbox_ip
		uman.hostmanager.aliases = [ "www." + "sitm" + ".local" ]

		# Set shared directories
		uman.vm.synced_folder "./src" , "/etc/sitm/", :mount_options => ["dmode=777", "fmode=666"]
		uman.vm.synced_folder ".", "/vagrant", :mount_options => ["dmode=777", "fmode=777"]

		uman.vm.provision :shell, :path => "provision/provision"
  end

	# manage /etc/hosts on guest for multi-node config
	config.vm.provision :hostmanager
end
