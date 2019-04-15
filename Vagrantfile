# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_API_VERSION = "2"

# Install Ansible on the guest
$ansible_install_script = <<-SCRIPT
export DEBIAN_FRONTEND=noninteractive
if ! command -v ansible >/dev/null 2>&1 ; then
    apt-get update -qq
    apt-get install -qq software-properties-common
    apt-add-repository ppa:ansible/ansible
    apt-get update -qq
    apt-get install -qq ansible
fi
SCRIPT

Vagrant.configure(VAGRANT_API_VERSION) do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.hostname = "flask-api-one-pager-demo"

    config.vm.network :forwarded_port, id: "flask",
        guest: 5000, host: 8080, auto_correct: true

    # Fix `stdin: is not a tty` warning
    # https://github.com/hashicorp/vagrant/issues/1673
    config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

    # Install Ansible (root)
    config.vm.provision "shell",
        inline: $ansible_install_script,
        privileged: true

    config.vm.provision "ansible_local" do |ansible|
        ansible_verbose = true
        ansible.playbook = "provisioning/playbook.yml"
    end

    config.vm.provider "virtualbox" do |vbox, override|
        vbox.name = config.vm.hostname   # vbox ui title
        vbox.gui = false
        vbox.memory = 1024
        vbox.cpus = 1
    end

    if Vagrant.has_plugin?("vagrant-vbguest")
        config.vbguest.auto_update = false
    end
end
