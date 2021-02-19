'''
SysLogHandler -> utilize syslog for logging p3 stanrart lib
https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler

linux:
    /dev/log

osx: 
    /var/run/syslog
'''

import os

import logging
import logging.handlers


class SyslogEventor:

    SYSLOG_LINUX_FILE_HANDLER = '/dev/log'
    SYSLOG_OSX_FILE_HANDLER = '/var/run/syslog'
    MAX_FILE_SIZE_BYTES = 10485760    # 10 Megabytes
    NUMBER_OF_BACKUPS = 7

    def __init__(self, logger_name=None):
        self.logger_name = logger_name
        if not logger_name:
            logger_name = f'{ __class__.__name__ }'

        # Note - https://docs.python.org/3/library/logging.html#logging.getLogger
        #   All calls to this function with a given name return the same logger instance. 
        #   This means that logger instances never need to be passed between different parts of an application.
        my_logger = logging.getLogger(logger_name)
        my_logger.setLevel(logging.INFO)


        # note the difference between sending via UDP and via TCP
        #     TODO note that if I'm going to sockets ->
        #     https://stackoverflow.com/a/42448463
        
        syslog_addr = self.__class__.__get_syslog_f()
        if not syslog_addr:
            raise Exception('Failed to find syslog socket/file descriptor during __init__')

        syslog_handler = logging.handlers.SysLogHandler(address = syslog_addr,
            facility=logging.handlers.SysLogHandler.LOG_USER)
        syslog_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        syslog_handler.setFormatter(syslog_formatter)
        my_logger.addHandler(syslog_handler)

        # adding additional file handler -> double the logging for redundancy.
        file_handler = logging.handlers.RotatingFileHandler(filename=f'{logger_name}.log',
            mode='a', encoding='utf-8',
            backupCount=self.NUMBER_OF_BACKUPS, maxBytes=self.MAX_FILE_SIZE_BYTES)
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(fh_formatter)
        my_logger.addHandler(file_handler)

        self.logger_name = logger_name

    def log_message(self, msg=None, close_file_handler=False):
        if not self.logger_name:
            # failed to iniate logger during __init__
            raise Exception('Failed to connect to existing logger')
        my_logger = logging.getLogger(self.logger_name)
        # TODO improve multiline output in syslog.
        my_logger.info(msg)
        # close connections if needed.
        if close_file_handler:
            [_handler.close() for _handler in my_logger.handlers]


    @classmethod
    def __get_syslog_f(cls):
        syslog_addr = None
        if os.path.exists(cls.SYSLOG_LINUX_FILE_HANDLER):
            syslog_addr = cls.SYSLOG_LINUX_FILE_HANDLER
        elif os.path.exists(cls.SYSLOG_OSX_FILE_HANDLER):
            syslog_addr = cls.SYSLOG_OSX_FILE_HANDLER
        return syslog_addr


if __name__ == "__main__":
    # execute only if run as a script
    print('py module to interact with syslog on rpi ubuntu.\n' +
        'Usage:\n' + 
        '\tmy_logger = SyslogEventor(\'<your logger name>\')\n' +
        '\tmy_logger.log_message(\'<Awesome message to log..>\')\n'
        )


