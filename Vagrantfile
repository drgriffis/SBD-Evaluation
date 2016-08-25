# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "hashicorp/precise64"
    config.vm.hostname = "SBDEvaluation"
    config.vm.provision :shell, path: "install/bootstrap.sh"
    config.vm.define "SBDEvaluation"  # Name the VM

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
    end
end
