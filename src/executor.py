from subprocess import Popen, PIPE
from datetime import datetime


class Executor(object):

    @classmethod
    def execute(cls, command):
        """
        Executing a given command and
        writing in a log file in cases where errors arise.
        """
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode:
            with open("failed_commands.log", 'a') as log:
                now = datetime.now()
                log.write('{}/{}/{} , {}:{}:{}\n\n'.format(now.day, now.month,
                                                           now.year, now.hour,
                                                           now.minute,
                                                           now.second))

                log.write("COMMAND:\n{}\n\n".format(" ".join(command)))
                log.write("OUTPUT:\n{}\n\n".format(output.decode("utf-8")))
                log.write("ERRORS:\n{}\n".format(err.decode("utf-8")))
                log.write('-'*40)
                log.write('\n')

            return ''

        if not output:
            output = " "

        return output
