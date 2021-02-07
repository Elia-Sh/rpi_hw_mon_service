

import time
from contextlib import contextmanager
import tracemalloc
import os

# import secrets ;import random; # simulate an output of vcgencmd command

from syslog_eventor import SyslogEventor
from rpi_vcgen_utils import VcgenCmd, VcgenCommandsConfig


# start recording memory profiler.
tracemalloc.start()

vcgencmd_config_list = [
     VcgenCmd(VcgenCommandsConfig.measure_clock_cmd,
                VcgenCommandsConfig.measure_clock_devices,
                consume_all_args = False),
     VcgenCmd(VcgenCommandsConfig.measure_volts_cmd,
                VcgenCommandsConfig.measure_volts_devices,
                consume_all_args = False),
     VcgenCmd(VcgenCommandsConfig.get_throttled_cmd),
     VcgenCmd(VcgenCommandsConfig.measure_temp_cmd),
     VcgenCmd(VcgenCommandsConfig.logs_status_cmd),
     VcgenCmd(VcgenCommandsConfig.pm_get_status_cmd),   
]

def sleep_for_seconds(n=20):
    '''
    '''
    time.sleep(n)
    return


@contextmanager
def run_step(step_text = '', step_num = None):
    # TODO maybe convert to Formatted String Literal (f-String) 
    STEP_PREFIX = 'STEP'
    step_str = STEP_PREFIX
    if step_num:
        step_str += ':{} '.format(str(step_num))
    step_str += str(step_text)
    print_to_console_and_log(step_str)
    yield
    # TODO step finished?

def is_py_ver_supported(py_version_tuple=(0,0)):
    '''
    Provide python as a tuple - i.e: is_py_ver_supported(3,6)
    '''
    tested_version_major, tested_version_minor = None, None
    is_supported = False
    if py_version_tuple and len(py_version_tuple) >= 2:
        # throw away user given extra version data -> need only major and minor python version.
        tested_version_major, tested_version_minor, *_ = py_version_tuple        
    else:
        # unexpected argument provided to is_py_ver_supported
        raise Exception('Testing version failed; please provide version to test in as tuple - i.e: (3,6)')
    
    system_version_major, system_version_minor, *more_version_info = sys.version_info
    if (system_version_major >= tested_version_major and 
        system_version_major >= tested_version_minor):
            is_supported = True
    return is_supported


def get_my_memory_stats():
    mem_usage_str = ''
    m_size, m_peak = tracemalloc.get_traced_memory()
    mem_usage_str = f'<<m_size: {m_size}, m_peak: {m_peak}>>'
    return(mem_usage_str)

def get_my_open_file_descriptors():
    '''
    python similar to lsof;
     TODO: consider adding file sizes and read/write state
    '''
    pid = os.getpid()
    fd_dir_path = f'/proc/{pid}/fd'
    open_file_descriptors = []
    for file_name in os.listdir(fd_dir_path):
        path_to_fd = os.path.join(fd_dir_path, file_name)
        open_file_descriptors.append(os.path.realpath(path_to_fd))
    return open_file_descriptors


def print_to_console_and_log(msg='', close_file_handler=False):
    '''
    Wrapper method to write to "both" - console and logging mechanism.
    '''
    print(msg)
    my_logger.log_message(msg, close_file_handler)

LOOP_ITERATOR_MAX = 5
SLEEP_TIMER = 10
log_file = 'rpi_loger_instance'
my_logger = SyslogEventor(log_file) # initialize log mechanism - syslog+log to separate log file.

step = 'Started monitoring service loop; (sleep timer: {})'.format(SLEEP_TIMER)
print_to_console_and_log(step)
current_memory_stats = get_my_memory_stats()
print_to_console_and_log(f'\t{current_memory_stats}')

for i in range(LOOP_ITERATOR_MAX):

    step = 'Started monitoring service cycle: {};'.format(i+1)
    print_to_console_and_log(step)
    
    open_file_descriptors = get_my_open_file_descriptors()
    open_fds_str = f'Open FileDescriptors: {len(open_file_descriptors)} -> {open_file_descriptors}'
    print_to_console_and_log(open_fds_str)

    for cmd_obj in vcgencmd_config_list:
        print_to_console_and_log(f'\trunning: {cmd_obj}')
        # simulation of command execution:
        # time.sleep(1)
        # output = secrets.token_bytes(random.randint(1,12))
        output = cmd_obj.run_vcgen_cmd()
        # import pdb; pdb.set_trace();
        print_to_console_and_log(f'\tResult: {str(output)}')

    step = 'sleeping for the:{} time;\n{}\n'.format(i+1,'*'*42)
    current_memory_stats = get_my_memory_stats()
    print_to_console_and_log(f'\t{current_memory_stats}')
    print_to_console_and_log(step, close_file_handler=True)
    sleep_for_seconds(SLEEP_TIMER)

step = 'Finished monitoring service loop;\n'
print_to_console_and_log(step)

current_memory_stats = get_my_memory_stats()
print_to_console_and_log(f'{current_memory_stats}')

open_file_descriptors = get_my_open_file_descriptors()
open_fds_str = f'Open FileDescriptors: {len(open_file_descriptors)} -> {open_file_descriptors}'
print_to_console_and_log(open_fds_str)




