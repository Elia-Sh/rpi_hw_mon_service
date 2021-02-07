
import subprocess

class VcgenCmd:

    VCGENCMD_PATH = '/usr/bin/vcgencmd'

    def __init__(self, vcgencmd_command, vcgencmd_args = [], consume_all_args = True):
        '''
            consume_all_args -> flag contorling over the command arguments need to send to vcgencmd,
                                meaning, !!!if the flag is set to False!!!
                                the execution should be -
                                vcgencmd <cmd> <arg1 from vcgencmd_args>;
                                vcgencmd <cmd> <arg2 from vcgencmd_args>;
                                etc...
                                vcgencmd <cmd> <arg[n] from vcgencmd_args>;
        '''
        self.output_str = ''
        self.consume_all_args = consume_all_args
        if vcgencmd_command:
            self.vcgencmd_command = vcgencmd_command
        else:
            raise Exception('{} must recieve vcgencmd_command '.format(self.__class__))

        if isinstance(vcgencmd_args, list):
            self.vcgencmd_args = vcgencmd_args
        elif isinstance(vcgencmd_args, str):
            self.vcgencmd_args = [vcgencmd_args]
        else:
            # not a list and not a single argument.
            # note that we "allow" empty args -> 
            # since empty args unpacked to None: 
            #       print(len(*['']))
            raise Exception('{} must get vcgencmd_args as a list '.format(self.__class__))

    def __repr__(self):
       return (f'<{self.__class__.__name__}('
               f'{self.vcgencmd_command!r}, {self.vcgencmd_args!r});>')

    def run_vcgen_cmd(self):
        '''
        Execute the command stored in the object instance,
        and store the output,
        Note - consume_all_args property controls the iteration over args.
        '''
        vcgencmd_full_cmd = []
        output_str = '' 
        if self.consume_all_args:
            # note the beautiful hack to construct a flat list. 
            a1_list = self.vcgencmd_command if isinstance(self.vcgencmd_command, list) else self.vcgencmd_command.split()
            a2_list = self.vcgencmd_args if isinstance(self.vcgencmd_args, list) else self.vcgencmd_args.split()
            vcgencmd_full_cmd = [self.__class__.VCGENCMD_PATH] + a1_list + a2_list
            # print('running: {}'.format(vcgencmd_full_cmd))
            output_str = self.__class__.__vcgen_cmd_executer(vcgencmd_full_cmd)
        else:
            # need to execute multiple commands - for each arg in vcgencmd_args
            for element in self.vcgencmd_args:
                constructed_cmd = [self.__class__.VCGENCMD_PATH, self.vcgencmd_command, element]
                current_cmd_output = self.__class__.__vcgen_cmd_executer(constructed_cmd)
                output_str = f'{output_str}{element}: {current_cmd_output}, '
            output_str = f'{output_str};'

        self.output_str = output_str
        return self.output_str

    @classmethod
    def is_vcgencmd_installed(cls):
        print('testing existance of: {}'.format(cls.VCGENCMD_PATH))
        is_installed = False
        try:
            subprocess.run(cls.VCGENCMD_PATH, timeout=10, check=True)
            is_installed = True
        except Exception:
            print('\'vcgencmd\' does not exist in path:'.format(cls.VCGENCMD_PATH))
        return is_installed


    @classmethod
    def __vcgen_cmd_executer(cls, full_vcgencmd_list = []):
        '''
        note that subprocess.run() prefers sequence of program arguments
        '''
        returned_output_str = ''
        if not full_vcgencmd_list or not isinstance(full_vcgencmd_list, list):
            raise Exception('Failed to pass arguments in as a list type')
        try:
            cmd_results = subprocess.run(full_vcgencmd_list, capture_output=True, text=True, timeout=10)
        except OSError as e:
            print('Execution error: {}'.format(e))
        except subprocess.SubprocessError as e:
            print('Execution error: {}'.format(e))

        if cmd_results.stdout:
            returned_output_str = cmd_results.stdout
        else:
            returned_output_str = cmd_results.stderr
        return cmd_results.stdout


    @classmethod
    def help(cls):
        '''
        method to display help for users.
        '''
        returned_str = 'Python module for communication with ' \
            + 'VideoCore GPU on the Raspberry Pi,\n via the \'vcgencmd\' command line utility'
        
        return returned_str


class VcgenCommandsConfig:
    '''
        $ vcgencmd commands; # lists available commands.
         
        https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
        https://github.com/raspberrypi/userland/blob/master/host_applications/linux/apps/gencmd/gencmd.c

    '''
    # some commands hav their own arguments - componets/etc
    measure_clock_cmd = 'measure_clock'
    measure_clock_devices = ['arm',
    'core',
    'h264',
    'isp',
    'v3d',
    'uart',
    'pwm',
    'emmc',
    'pixel',
    'vec',
    'hdmi',
    'dpi',]
    ''' Clock   Description
        ______  ________________________________
        arm     ARM cores
        core    VC4 scaler cores
        h264    H.264 block
        isp     Image Signal Processor
        v3d     3D block
        uart    UART
        pwm     PWM block (analog audio output)
        emmc    SD card interface
        pixel   Pixel valve
        vec     Analog video encoder
        hdmi    HDMI
        dpi     Display Peripheral Interface'''

    measure_volts_cmd = 'measure_volts'
    measure_volts_devices = ['core',
    'sdram_c',
    'sdram_i',
    'sdram_p',]

    get_throttled_cmd = 'get_throttled'
    '''vcgencmd get_throttled
        A value of zero indicates that none of the above conditions is true.
        Bit  Hex value  Meaning
        0    1          Under-voltage detected
        1    2          Arm frequency capped
        2    4          Currently throttled
        3    8          Soft temperature limit active
        16   10000      Under-voltage has occurred
        17   20000      Arm frequency capping has occurred
        18   40000      Throttling has occurred
        19   80000      Soft temperature limit has occurred'''
    measure_temp_cmd = 'measure_temp'
    logs_status_cmd = 'vcos log status' # Note the spacing in the "arguments.."
    pm_get_status_cmd = 'pm_get_status'


    @classmethod
    def help(cls):
        class_name_str = cls.__name__
        # helper method to print commands and arguments that declared in the py module.
        prop_list = [element for element in vars(cls) if not element.startswith('__')]
        prop_list.remove('help') # remove this method - since it's not a property of the config. 
        output_str = ' vcgencmd commands and their arguments -> as declared at {};\n'.format(class_name_str)
        # import pdb; pdb.set_trace();
        for prop_key in prop_list:
            current_prop = vars(cls)[prop_key]
            current_prop_str = ''
            if isinstance(current_prop, list):
                current_prop_str = '{}.{}\t{}'.format(class_name_str, prop_key, str(current_prop))
            else:
                current_prop_str = '{}.{}\t\t{}'.format(class_name_str, prop_key, str(current_prop))
            output_str = output_str + current_prop_str + '\n'
        return(output_str)

####
#### 
if __name__ == "__main__":
    print(VcgenCmd.help())
    print(VcgenCommandsConfig.help())

# some debugging code snippets - 
# # vcgencmd_command_volts_obj = VcgenCmd(vcgencmd_command_volts1, volts_dev_name_arr, consume_all_args = False)
# # vcgencmd_command_volts_obj.run_vcgen_cmd()
# zibi = VcgenCmd(['vcos', 'log','status'])
# bibi = VcgenCmd('vcos log status') # -> not storing the output/ not running the cmd.
# bibi.run_vcgen_cmd()
# vcgencmd_config_list = [
#     VcgenCmd(vcgencmd_command_clock1, clock_dev_name_arr, consume_all_args = False),
#     VcgenCmd(vcgencmd_command_volts1, volts_dev_name_arr, consume_all_args = False),
#     VcgenCmd('get_throttled'),
#     VcgenCmd('measure_temp'),
#     VcgenCmd('pm_get_status'),
#     VcgenCmd('vcos log status'),   
# ]

# # execute all commands - 
# [elm.run_vcgen_cmd() for elm in vcgencmd_config_list]

