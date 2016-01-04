# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "hashicorp/precise64"
    config.vm.hostname = "ClinicalSBD"
    config.vm.provision :shell, path: "install/bootstrap.sh"
end
