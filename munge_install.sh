#install
yum install munge munge-devel

#create random key (only in master)  
dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key
chown munge /etc/munge/munge.key

#Copy the key to every computing element (only in master, to every computing element)
 scp /etc/munge/munge.key root@COMPUTING-ELEMENT:/etc/munge/munge.key
 chown munge /etc/munge/munge.key


#create required folders
mkdir /var/run/munge/
chown munge /var/run/munge/

#permission fix
chmod 400 /etc/munge/munge.key
chmod 711 /var/lib/munge/
chmod 755 /var/run/munge/

#make it start on system boot
service munge start
chkconfig  munge on
