import os
import sys
import datetime
import tempfile

from optparse import OptionParser
from copy import deepcopy

from ConfigParser import ConfigParser

from benchmaster.utils import run_command, run_pssh, run_fl_build_report

def get_options():
    """Parse command line options and return an options object
    """
    
    usage = """\
Usage: %prog [options] <nodes file> <test file> [<test name>]

The nodes file is a PSSH nodes file list.

The test file should be a Funkload test file. It should follow the Funkload
recorder naming conventions, and must live in the same directory as the
bench test configuration file.
"""
    
    parser = OptionParser(usage=usage)
    
    parser.add_option("-n", "--name", dest="name", default="",
            help="Name of the bench run. Defaults to {timestamp}-{test}", 
        )
    parser.add_option("-c", "--cycles", dest="cycles", default=1,
            help="Override the bench bench cycles from the bench test configuration file, this is a list of number of virtual concurrent users, to run a bench with 3 cycles with 5, 10 and 20 users use: -c 5:10:20"
        )
    parser.add_option("-D", "--duration", dest="duration", default=60,
            help="Override duration of a cycle (in seconds) from the test configuration file"
        )
    parser.add_option("-w", "--working-directory", dest="working_dir", default=os.getcwd(),
            help="Working directory. Defaults to the current directory."
        )
    parser.add_option("-x", "--node-working-directory", dest="node_working_dir", default="/tmp/bench-node",
            help="Node working directory. Will be created on the node if it does not exist. Defaults to /tmp/bench-node."
        )
    parser.add_option("-s", "--node-script", dest="node_script", default="bench-node",
            help="Path to the bench-node script on each node. Defaults to looking for the script in the system path."
        )
    parser.add_option("-u", "--url", dest="url",
            help="Override the base URL from the bench test configuration file"
        )
    parser.add_option("--num-nodes", dest="nodes", type="int",
            help="Maximum number of nodes to use from the nodes file",
        )
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
            help="Verbose output"
        )
    
    options, args = parser.parse_args()
    
    if len(args) < 2:
        print "[ERROR] You must specify the nodes and test files"
        sys.exit(1)
    
    if len(args) > 2:
        print "[ERROR] Unexpected command line arguments"
        sys.exit(1)
    
    if not os.path.isdir(options.working_dir):
        print "[ERROR] Working directory", options.working_dir, "not found"
        sys.exit(1)
    
    options.nodes_file = args[0]
    if not os.path.isfile(options.nodes_file):
        print "[ERROR] Nodes file", options.nodes_file, "not found"
        sys.exit(1)
    
    options.test_file = args[1]
    if not os.path.isfile(options.test_file):
        print "[ERROR] Test file", options.test_file, "not found"
        sys.exit(1)
    
    options.test_file_path = os.path.dirname(options.test_file)
    
    if len(args) >= 3:
        options.test_name = args[2]
    else:
        options.test_name = os.path.splitext(os.path.basename(options.test_file))[0][5:]
        
    options.config_file = "%s.conf" % options.test_name
    if options.test_file_path:
        options.config_file = os.path.join(options.test_file_path, options.config_file)    
    if not os.path.isfile(options.config_file):
        print "[ERROR] Config file", options.config_file, "not found"
        sys.exit(1)
    
    if not options.name:
        stamp = datetime.datetime.now().isoformat().replace(':', '-')
        options.name = "%s-%s" % (stamp, options.test_name,)
    
    return options

def main():
    """This is the main script, installed as the ``bench-master`` console
    script.
    """

    options = get_options()
    
    run_name = options.name
    
    master_test_module_path = options.test_file
    master_test_config_path = options.config_file
    master_node_config_path = options.nodes_file
    
    node_command_path  = options.node_script
    node_working_dir   = options.node_working_dir
    node_run_base_path = os.path.join(node_working_dir, run_name)
    
    # Create a PSSH nodes configuration specifically for this run
    run_node_config = tempfile.NamedTemporaryFile(delete=False)
    nodes_master = open(master_node_config_path, 'r').read().splitlines()
    nodenum = 0
    for line in nodes_master:
        if options.nodes and nodenum >= options.nodes:
            break
    
        run_node_config.write(line+'\n')
        nodenum += 1
    
    run_node_config_path = run_node_config.name
    run_node_config.close()
    
    master_run_path = os.path.join(options.working_dir, run_name)
    master_run_results_path = os.path.join(master_run_path, "results")
    master_run_stdout_path = os.path.join(master_run_path, "out")
    master_run_stderr_path = os.path.join(master_run_path, "err")
    
    for mkdir_path in (options.working_dir, master_run_path, master_run_stdout_path, master_run_stderr_path, master_run_results_path,):
        if not os.path.exists(mkdir_path):
            os.makedirs(mkdir_path)
    
    nodes = open(run_node_config_path, 'r').read().splitlines()
    
    print "\n\n### Deploying benchmark: %s ###\n\n" % run_name
    
    master_test_config = ConfigParser()
    master_test_config.read(master_test_config_path)
    for nodenum, line in enumerate(nodes):
        node_test_config = deepcopy(master_test_config)
        
        node_host = line.split(' ')[0]
        node_user = line.split(' ')[-1]
        
        node_run_path = os.path.join(node_run_base_path, "node%i" % nodenum)
        
        run_command('ssh %(node_user)s@%(node_host)s mkdir -p %(node_run_path)s' % dict(
                node_user=node_user,
                node_host=node_host,
                node_run_path=node_run_path,
            ), print_stderr=True)
        
        run_command('scp %(master_test_module_path)s %(node_user)s@%(node_host)s:%(node_run_path)s' % dict(
                master_test_module_path=master_test_module_path,
                node_user=node_user,
                node_host=node_host,
                node_run_path=node_run_path,
            ), print_stderr=True)
        
        node_test_config.set('bench', 'node_num', nodenum)
        
        # Only run the monitor on the first node
        if nodenum != 0:
            if node_test_config.has_option('monitor', 'hosts'):
                node_test_config.remove_option('monitor', 'hosts')
        
        if options.url:
            node_test_config.set('main', 'url', options.url)
        
        if options.cycles:
            node_test_config.set('bench', 'cycles', options.cycles)
        
        if options.duration:
            node_test_config.set('bench', 'duration', options.duration)
        
        node_test_config_tempfile = tempfile.NamedTemporaryFile(delete=False)
        node_test_config.write(node_test_config_tempfile)
        node_test_config_path = node_test_config_tempfile.name
        node_test_config_tempfile.close()
        
        run_command('scp %(node_test_config_path)s %(node_user)s@%(node_host)s:%(node_run_path)s/%(master_test_config_filename)s' % dict(
                node_test_config_path=node_test_config_path,
                node_user=node_user,
                node_host=node_host,
                node_run_path=node_run_path,
                master_test_config_filename=os.path.basename(master_test_config_path),
            ), print_stderr=True)
        
        os.unlink(node_test_config_path)
    
    print "\n\n### Running benchmark: %s ###\n\n" % run_name
    
    # Set up environment to be marshalled to each node
    environ = {
        'PSSH_BENCH_RUN': run_name,
        'PSSH_BENCH_WORKING_DIR': node_working_dir,
    }
    
    # Set up the command to run
    
    # Note: %(nodenum)s gets replaced by the node number when the parallelisation kicks in
    node_cmd = '%s "%s" "%s" "%%(nodenum)s" %s' % (node_command_path, node_working_dir, run_name, options.test_name)
    
    run_pssh(node_cmd, run_node_config_path, master_run_stdout_path, master_run_stderr_path, environ)
    
    print "\n\n### Collating results for: %s ###\n\n" % run_name
    for nodenum, line in enumerate(nodes):
        host = line.split(' ')[0]
        user = line.split(' ')[-1]
        
        node_run_path = os.path.join(node_run_base_path, "node%i" % nodenum)
        node_log_file_path = os.path.join(node_run_path, '*.xml')
        
        run_command('scp %(user)s@%(host)s:%(node_log_file_path)s %(master_run_results_path)s/node_%(nodenum)i.xml' % dict(
                user=user,
                host=host,
                node_log_file_path=node_log_file_path,
                master_run_results_path=master_run_results_path,
                nodenum=nodenum,
            ))
    
    html_report_path = os.path.join(master_run_path, "report")
    if not os.path.exists(html_report_path):
        os.makedirs(html_report_path)
    
    print "\n\n### Compiling report for: %s\n\n" % run_name
    
    run_fl_build_report(os.path.join(master_run_results_path, '*.xml'), html_report_path)
    
    print "\n\n###Report complete: %s" % (run_name,)
    
    # Clean up
    os.unlink(run_node_config_path)
