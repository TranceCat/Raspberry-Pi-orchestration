import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import json


utils.VERBOSITY = 0
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
stats = callbacks.AggregateStats()
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)


inventory = ansible.inventory.Inventory("./inventory.py")

# run modules
pm = ansible.runner.Runner(
    module_name = 'ping', #'command',
    #module_args = 'uname -a',
    inventory = inventory,
    pattern = "all" 
    )

out = pm.run()
print json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))


#
#pb = ansible.playbook.PlayBook(
#	playbook= "./main.yml",
#	callbacks=playbook_cb,
#    runner_callbacks=runner_cb,
#	stats=stats,
#    inventory = inventory
#	)
#out = pb.run()
#
#playbook_cb.on_stats(pb.stats)
#print out



