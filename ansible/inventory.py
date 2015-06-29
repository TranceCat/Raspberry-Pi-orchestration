#!/usr/bin/env python
'''
Ansible dynamic inventory experimentation

Output dynamic inventory as JSON from statically defined data structures
'''

import argparse
import json
import sys
sys.path.append('../rpi/')
import rpi_detector

#ANSIBLE_INV = {
#    "rpi": {
#        "hosts": ["rpi1", "rpi2", "rpi3", "rpi4"],
#        "vars": {
#            "ansible_ssh_user": "root",
#            "ansible_ssh_private_key_file":"~/.ssh/dd_wrt"
#
#        }
#    }
#}
#
#HOST_VARS = {
#    "rpi1": {"ansible_ssh_host": "10.0.0.17"},
#    "rpi2": {"ansible_ssh_host": "10.0.0.101"},
#    "rpi3": {"ansible_ssh_host": "10.0.0.105"},
#    "rpi4": {"ansible_ssh_host": "10.0.0.135"},
#}


def output_list_inventory(json_output):
    '''
    Output the --list data structure as JSON
    '''
    print json.dumps(json_output)


def find_host(search_host, inventory):
    '''
    Find the given variables for the given host and output them as JSON
    '''
    host_attribs = inventory.get(search_host, {})
    print json.dumps(host_attribs)


def main():
    '''
    Ansible dynamic inventory experimentation

    Output dynamic inventory as JSON from statically defined data structures
    '''

    # Argument parsing
    parser = argparse.ArgumentParser(description="Ansible dynamic inventory")
    parser.add_argument("--list", help="Ansible inventory of all of the groups",
                        action="store_true", dest="list_inventory")
    parser.add_argument("--host", help="Ansible inventory of a particular host", action="store",
                        dest="ansible_host", type=str)

    cli_args = parser.parse_args()
    list_inventory = cli_args.list_inventory
    ansible_host = cli_args.ansible_host

    rpi_detector.run()
    ANSIBLE_INV= rpi_detector.var_gen_inv()
    HOST_VARS = rpi_detector.var_gen_host()
    if list_inventory:
        output_list_inventory(ANSIBLE_INV)

    if ansible_host:
        find_host(ansible_host, HOST_VARS)


if __name__ == "__main__":
    main()