#  Install Maria DB
yum install mariadb-server mariadb-devel -y

#  Create Global Users
export MUNGEUSER=991
groupadd -g $MUNGEUSER munge
useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u $MUNGEUSER -g munge  -s /sbin/nologin munge
export SLURMUSER=992
groupadd -g $SLURMUSER slurm
useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u $SLURMUSER -g slurm  -s /bin/bash slurm

#  Get EPEL rep
yum install epel-release

#  Install Munge
yum install munge munge-libs munge-devel -y

#  Create a secret key (skip)
'''
yum install rng-tools -y
rngd -r /dev/urandom
'''

#  Create munge key    removed -r
sudo su -c '/usr/sbin/create-munge-key' 
sudo su -c 'dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key'
sudo su -c 'chown munge: /etc/munge/munge.key'
sudo su -c 'chmod 400 /etc/munge/munge.key'

#Distribute munge key
#  scp /etc/munge/munge.key root@1.buhpc.com:/etc/munge
#  scp /etc/munge/munge.key root@1.compute-1.assign-5.pdc-edu-lab-pg0.clemson.cloudlab.us

scp /etc/munge/munge.key BC843101@compute-1:/etc/munge
scp /etc/munge/munge.key BC843101@compute-2:/etc/munge

#Munge permissions for nodes
chown -R munge: /etc/munge/ /var/log/munge/
chmod 0700 /etc/munge/ /var/log/munge/

#  Start Munge
systemctl enable munge
systemctl start munge

''' Test Munge
munge -n
munge -n | unmunge
munge -n | ssh 3.buhpc.com unmunge
remunge
'''

#  Slurm dependencies
yum install openssl openssl-devel pam-devel numactl numactl-devel hwloc hwloc-devel lua lua-devel readline-devel rrdtool-devel ncurses-devel man2html libibmad libibumad -y

#  Install Slurm
cd /nfs
wget http://www.schedmd.com/download/latest/slurm-15.08.9.tar.bz2

#  Install rpmbuild
yum install rpm-build
rpmbuild -ta slurm-15.08.9.tar.bz2

