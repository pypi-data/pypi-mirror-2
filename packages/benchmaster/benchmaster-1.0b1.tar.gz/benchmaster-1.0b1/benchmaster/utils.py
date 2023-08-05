import os
import sys
import tempfile

from glob import glob
from copy import deepcopy

from subprocess import Popen
from subprocess import PIPE

from psshlib import psshutil
from psshlib.manager import Manager
from psshlib.task import Task

from funkload.BenchRunner import BenchRunner
from funkload.ReportBuilder import FunkLoadXmlParser
from funkload.MergeResultFiles import MergeResultFiles
from funkload.ReportRenderHtml import RenderHtml

def run_command(command, print_stdout=False, print_stderr=False, verbose=False):
    """Run a command in a subprocess, optionally printing its stdout/stderr
    """
    
    if verbose:
        print "Running:", command
    
    print_stdout = print_stdout or verbose
    print_stderr = print_stderr or verbose
    
    stdout = None
    stderr = None
    
    if print_stdout:
        stdout = PIPE
    if print_stderr:
        stderr = PIPE
    
    p = Popen(command, shell=True, stdin=None, stdout=stdout, stderr=stderr, close_fds=True)
    
    out, err = p.communicate()
    
    if print_stdout:
        print out
    
    if print_stderr:
        print >> sys.stderr, err

def run_pssh(cmdline, hosts_file, stdout_path, stderr_path, environ):
    """Run a PSSH session.
    
    cmdline is the remote command to run.
    hosts_file is the file containing the node entries
    stdout_path and stderr_path are files for stdout and stderr
    environ is a dict of additional environment variables, which will be
      marshalled to the nodes
    """
    
    class FauxOpts(object):
        par       = 32
        timeout   = None
        outdir    = stdout_path
        errdir    = stderr_path
        user      = None
        verbose   = True
        print_out = True
        inline    = False
        askpass   = False
        
        def __getattr__(self, name):
            return None
    
    opts = FauxOpts()
    
    hosts = psshutil.read_hosts([hosts_file])
    
    if not os.path.exists(opts.outdir):
        os.makedirs(opts.outdir)
    if not os.path.exists(opts.errdir):
        os.makedirs(opts.errdir)
    
    stdin = ""
    
    manager = Manager(opts)
    for nodenum, (host, port, user,) in enumerate(hosts):
        
        cmd = ['ssh', host, '-o', 'NumberOfPasswordPrompts=1']
        
        if user:
            cmd += ['-l', user]
        if port:
            cmd += ['-p', port]
        
        # Tell SSH to marshall out environment variables
        
        cmd += ['-o', 'SendEnv=PSSH_NODENUM']
        
        for key in environ:
            cmd += ["-o", "SendEnv=" + key]
        
        cmd.append(cmdline % {'nodenum': nodenum})
        
        t = Task(host, port, user, cmd, opts, stdin)
        manager.add_task(t)
    
    # Temporarily update our environment so that the sub-process inherits
    # the right thing. 
    
    old_environ = deepcopy(os.environ)
    os.environ.update(environ)
    
    manager.run()
    
    os.environ.clear()
    os.environ.update(old_environ)

def run_fl_build_report(input_path, output_path):
    """Create an HTML report from the input file(s) at input_path (wildcards
    accepted), outputting it to the directory specified as output_path
    """
    
    
    input_files = glob(input_path)
    
    if len(input_files) == 0:
        print >> sys.stderr, "[ERROR] Cannot find report XML files in", input_path
        return
    
    class FauxOpts(object):
        apdex_t          = 1.5
        output_dir       = output_path
        html             = True
        with_percentiles = True
        diffreport       = False
        report_dir       = None
        
        def __getattr__(self, name):
            return None
    
    opts = FauxOpts()
    
    # Merge files if necessary
    if len(input_files) > 1:
        f = tempfile.NamedTemporaryFile(prefix='fl-mrg-', suffix='.xml')
        tmp_file = f.name
        f.close()
        MergeResultFiles(input_files, tmp_file)
        opts.xml_file = tmp_file
    else:
        opts.xml_file = input_files[0]
    
    try:
        xml_parser = FunkLoadXmlParser(1.4)
    except TypeError: # funkload < 0.13
        xml_parser = FunkLoadXmlParser()
    
    xml_parser.parse(opts.xml_file)
    
    RenderHtml(
            xml_parser.config,
            xml_parser.stats,
            xml_parser.error,
            xml_parser.monitor,
            opts)()

def run_fl_run_bench(test_module, test_class, test_method, color=False):
    """Execute the Funkload bench runner
    """
    
    class FauxOpts(object):
        no_color = not color
        debugserver = None
        debugport = None
        
        # taken from config file
        main_url = None
        bench_cycles = None
        bench_duration = None
        bench_sleep_time_min = None
        bench_sleep_time_max = None
        bench_sleep_time = None
        bench_startup_delay = None
        as_fast_as_possible = None
        accept_invalid_links = None
        simple_fetch = None
        label = None
        
        def __getattr__(self, name):
            return None
    
    opts = FauxOpts()
    
    bench = BenchRunner(test_module, test_class, test_method, opts)
    
    ret = None
    try:
        ret = bench.run()
    except KeyboardInterrupt:
        print >> sys.stderr, "* ^C received *"
    
    return ret
