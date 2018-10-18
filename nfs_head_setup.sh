sudo yum -y install nfs-utils nfs-utils-lib
sudo yum -y install portmap

/etc/init.d/portmap start
/etc/init.d/nfs start
sudo chkconfig --level 35 portmap on
sudo chkconfig --level 35 nfs on

sudo mkdir /software
sudo chmod 777 /software

sudo systemctl enable nfs-server.service
sudo systemctl start nfs-server.service

echo '
/software 192.168.1.3(rw,sync,no_root_squash)
/software 192.168.1.4(rw,sync,no_root_squash)
/software 192.168.1.5(rw,sync,no_root_squash)
/software 192.168.1.6(rw,sync,no_root_squash)
/software 192.168.1.7(rw,sync,no_root_squash)
/software 192.168.1.8(rw,sync,no_root_squash)
/software 192.168.1.9(rw,sync,no_root_squash)
/software 192.168.1.10(rw,sync,no_root_squash)
/software 192.168.1.11(rw,sync,no_root_squash)
/software 192.168.1.12(rw,sync,no_root_squash)
/software 192.168.1.13(rw,sync,no_root_squash)
/software 192.168.1.14(rw,sync,no_root_squash)
/software 192.168.1.15(rw,sync,no_root_squash)' >> /etc/exports

sudo exportfs -a
