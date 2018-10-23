# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides the template for a full research cluster with head node, scheduler, compute nodes, and shared file systems.
First node (head) should contain: 
- Shared home directory using Networked File System
- Management server for SLURM
Second node (metadata) should contain:
- Metadata server for SLURM
Third node (storage):
- Shared software directory (/software) using Networked File System
Remaining three nodes (computing):
- Compute nodes  
"""
#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

link = request.LAN("lan")

for i in range(0, 15):
		
	if i == 0:
		node = request.XenVM("head")
		node.routable_control_ip = "true"
		# addServices to create NFS server on head node (directory: /software)
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/nfs_head_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs_head_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/nfs_storage_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs_storage_setup.sh "))
		
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountHead.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountHead.sh"))
		# Called in head node to immediately allow it to SSH
		node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
		# copy files to scratch
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /users/BC843101/scratch"))
		#node.addService(pg.Execute(shell="sh", command="sudo systemctl restart nfs-server.service"))
		# addServices to install MPI in the /software directory on head node
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
	elif i == 1:
		node = request.XenVM("metadata")
		# Metadata node, maybe remove later?
	elif i == 2:
		node = request.XenVM("storage")
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/nfs_head_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs_head_setup.sh"))
		
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountStorage.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountStorage.sh"))
		
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/nfs_storage_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs_storage_setup.sh "))

		# copy files to scratch
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /users/BC843101/scratch"))
	else:
		# compute-num nodes
		node = request.XenVM("compute-" + str(i-2))
		node.cores = 4
		node.ram = 4096
		node.addService(pg.Execute(shell="sh", command="sleep 5m"))
		node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/nfs_client_setup.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs_client_setup.sh"))
		# addServices to call bash scripts to add local mount points to client nodes for NFS's		
		# copy files to scratch
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
		node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /users/BC843101/scratch"))
		
	node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"

	iface = node.addInterface("if" + str(i))
	iface.component_id = "eth1"
	iface.addAddress(pg.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
	link.addInterface(iface)
	
	#Prevent Redundant call in head node
	if i != 0:
		node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
		node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
		#node.addService(pg.Execute(shell="sh", command="sudo systemctl restart nfs-server.service"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
