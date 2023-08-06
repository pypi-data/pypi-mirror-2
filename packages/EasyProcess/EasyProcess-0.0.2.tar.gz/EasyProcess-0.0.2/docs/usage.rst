Usage
==================


::

    >>> from easyprocess import EasyProcess

Run program, wait for it to complete, get stdout (command is string)::

    >>> EasyProcess('echo hello').call().stdout
    'hello'

Run program, wait for it to complete, get stdout (command is list)::

    >>> EasyProcess(['echo','hello']).call().stdout
    'hello'

Run program, wait for it to complete, get stderr::

    >>> EasyProcess('python --version').call().stderr
    'Python 2.6.6'

Run program, wait for it to complete, get return code::

    >>> EasyProcess('python --version').call().return_code
    0

Run program, wait 1 second, stop it, get stdout::

    >>> EasyProcess('ping localhost').start().sleep(1).stop().stdout
    'PING localhost.localdomain (127.0.0.1) 56(84) bytes of data.\n64 bytes from localhost.localdomain (127.0.0.1): icmp_req=1 ttl=64 time=0.026 ms'

Run program, wait for it to complete, check for errors::

    >>> EasyProcess('ls').check()
    True
    >>> EasyProcess('bad_command').check()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "easyprocess.py", line 84, in check
        raise EasyProcessCheckError(self)
    easyprocess.EasyProcessCheckError: EasyProcess check failed!
     OSError:[Errno 2] No such file or directory
     cmd:['bad_command']
     return code:None
     stderr:None
    >>> EasyProcess('sh -c bad_command').check()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "easyprocess.py", line 84, in check
        raise EasyProcessCheckError(self)
    easyprocess.EasyProcessCheckError: EasyProcess check failed!
     OSError:None
     cmd:['sh', '-c', 'bad_command']
     return code:127
     stderr:sh: bad_command: not found

Logging
=========

Example program:

.. literalinclude:: ../easyprocess/examples/log.py

Output:

.. program-output:: python -m easyprocess.examples.log
    :prompt:


Replacing existing functions
====================================

Replacing os.system::

    retcode = os.system("ls -l")
    ==>
    p = EasyProcess("ls -l").call()
    retcode = p.return_code
    print p.stdout

Replacing subprocess.call::

    retcode = subprocess.call(["ls", "-l"])
    ==>
    p = EasyProcess(["ls", "-l"]).call()
    retcode = p.return_code
    print p.stdout
