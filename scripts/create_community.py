import subprocess

# This script shows how to interact with the communityManagement MIB. First, it uses the the default master community,
# "admin", to update it with a new value. Then, it uses this new master community to create a new community with
#  read and write privileges to objects in the filter group.


# Agent IP address
ip_addr = ""

# Current master community. It is set as admin by default at installation time.
old_master_community = "admin"

# New master community that would be used to define new communities and assign privileges to them.
new_master_community = ""

# New community that would be used to edit the filter group
community = ""



#############################
#  Change master community  #
#############################

# Update the master community with a new value.
subprocess.call(["snmpset", "-v", "1", "-c", old_master_community, ip_addr, "1.3.6.1.4.1.28308.1.0", "s", new_master_community])


##########################
#  Create new community  #
##########################

# Create a new row in the communityTable (the communityStatus works as a RMON entryStatus). This table has two different
# indexes, the name of the new community (the ASCII representation of each letter in the community name concatenated by
# dots) and an unique identifier. There might be more than one row associated to the same community, each assigning
# different rights (view + permissions).
subprocess.call(["snmpset", "-v", "1", "-c", new_master_community, ip_addr, "1.3.6.1.4.1.28308.2.1.6.\'"+community+"\'.1", "i", "2"])

# Set Read-write permissions this row (0: No permissions, 1: Read access, 2: Write access, 3: Read-write)
subprocess.call(["snmpset", "-v", "1", "-c", new_master_community, ip_addr, "1.3.6.1.4.1.28308.2.1.4.\'"+community+"\'.1", "i", "3"])

# Set the view associated to this row. All the objects in the filter group (1.3.6.1.2.1.16.7) would be affected by this row.
subprocess.call(["snmpset", "-v", "1", "-c", new_master_community, ip_addr, "1.3.6.1.4.1.28308.2.1.5.\'"+community+"\'.1", "s", "1.3.6.1.2.1.16.7"])

# The row is set as active using the communityStatus.
subprocess.call(["snmpset", "-v", "1", "-c", new_master_community, ip_addr, "1.3.6.1.4.1.28308.2.1.6.\'"+community+"\'.1", "i", "1"])



##########################
#  Delete the community  #
##########################

# Delete the community that we just created
subprocess.call(["snmpset", "-v", "1", "-c", new_master_community, ip_addr, "1.3.6.1.4.1.28308.2.1.6.\'"+community+"\'.1", "i", "4"])