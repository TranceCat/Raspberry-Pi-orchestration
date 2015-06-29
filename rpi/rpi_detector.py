import subprocess
import os
import platform
import re


HOST_VARS = {}
ANSIBLE_INV = {}
rpi_ip_list = []
rpi_name_list = []

def nmap():
	t = subprocess.Popen("nmap -sP 10.0.0.0/24",shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	t.wait()

def pi_search():
	#print ('Searching for RPi')
	#print ("---------------------------")
	p = subprocess.Popen("arp -a | cut -f 2,4 -d ' ' ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		if line[-18:].startswith('b8:27:eb'):#eth0 mac : b8:27:eb
			ip_is = str(re.findall( r'[0-9]+(?:\.[0-9]+){3}',line))[2:-2]
			rpi_ip_list.append(ip_is)
			#print ("This is RPi IP: " + ip_is)
	#print ("---------------------------")
def var_gen_host():
	for i in range(len(rpi_ip_list)):
		rpi_name_list.append("rpi"+str(i))
		HOST_VARS[rpi_name_list[i]] = {}
		for k in range(len(rpi_name_list)):
			HOST_VARS[rpi_name_list[i]]['ansible_ssh_host']=rpi_ip_list[k]

	return (HOST_VARS)

def var_gen_inv():
	ANSIBLE_INV ["rpi"]={}
	ANSIBLE_INV ["rpi"]["hosts"]=rpi_name_list
	ANSIBLE_INV ["rpi"]["vars"] = {
	            "ansible_ssh_user": "root",
	            "ansible_ssh_private_key_file":"~/.ssh/dd_wrt"
				}
	return (ANSIBLE_INV)


def var_gen():
	var_gen_host()
	var_gen_inv()
	

def run():
	pi_search()

	if rpi_ip_list == []:
		nmap()
		pi_search()

def main():
	pi_search()

	if rpi_ip_list == []:
		print ('Runing nmap')
		nmap()
		pi_search()

	var_gen()
	print ("HOST_VARS")
	print (HOST_VARS)
	print ("ANSIBLE_INV")
	print (ANSIBLE_INV)
	#return (HOST_VARS,ANSIBLE_INV)


if __name__ == "__main__":
    main()
