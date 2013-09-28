# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box_url = "http://titan.nuspace.de/vagrant/debian-7.1.0-amd64.box"
  config.vm.box = "debian71amd"

  config.vm.synced_folder ".", "/home/vagrant/dev/"
  config.vm.network :forwarded_port, guest: 8000, host: 8000
end
