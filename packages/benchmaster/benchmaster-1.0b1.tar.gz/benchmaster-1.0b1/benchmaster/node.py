import os
import sys

from benchmaster.utils import run_fl_run_bench

def main():
    """This is the main script, installed as the ``bench-node`` console
    script.
    """
    
    if len(sys.argv) != 5:
        print >> sys.stderr, "[ERROR] Unexpected number of arguments"
        print >> sys.stderr, "Usage: %s <working dir> <run name> <node number> <test name>" % sys.argv[0]
    
    working_dir = sys.argv[1]
    run_name    = sys.argv[2]
    node_num    = sys.argv[3]
    test_name   = sys.argv[4]
    
    run_path = os.path.join(working_dir, run_name, "node%s" % node_num)
    
    if not os.path.isdir(run_path):
        print >> sys.stderr, "[ERROR] Cannot find run path", run_path, "- test not deployed?"
        sys.exit(1)
    
    # Put us in the right directory for funkload to find the config file
    os.chdir(run_path)
    
    config_files = [filename for filename in os.listdir(os.getcwd()) if filename.endswith('.conf')]
    
    if len(config_files) == 0:
        print >> sys.stderr, "[ERROR] No .conf file found in", run_path
        sys.exit(1)
    
    if len(config_files) > 1:
        print >> sys.stderr, "[ERROR] Too many .conf files found in", run_path
        sys.exit(1)
    
    # Make sure funkload can load the test module
    sys.path.insert(0, run_path)
    
    test_config_name = config_files[0]
    test_class = test_config_name[:-5]
    test_module = "test_%s.py" % test_class
    test_method = "test_%s" % test_name
    
    run_fl_run_bench(test_module, test_class, test_method, color=False)
