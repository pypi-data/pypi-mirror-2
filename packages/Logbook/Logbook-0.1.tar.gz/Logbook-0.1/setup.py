"""
Logbook
-------

An awesome logging implementation that is fun to use.

Quickstart
``````````

::

    from logbook import Logger
    log = Logger('A Fancy Name')

    log.warn('Logbook is too awesome for most applications')
    log.error("Can't touch this')

Works for Webapps too
`````````````````````

::

    from logbook import MailHandler

    mailhandler = MailHandler(from_addr='servererror@example.com',
                              recipients=['admin@example.com'],
                              level='ERROR', format_string=u'''\
Subject: Application Error for {record.extra[path]} [{record.extra[method]}]

Message type:       {record.level_name}
Location:           {record.filename}:{record.lineno}
Module:             {record.module}
Function:           {record.func_name}
Time:               {record.time:%Y-%m-%d %H:%M:%S}
Remote IP:          {record.extra[ip]}
Request:            {record.extra[path]} [{record.extra[method]}]

Message:

{record.message}
    ''')

    def handle_request(request):
        def inject_extra(record, handler):
            record.extra['ip'] = request.remote_addr
            record.extra['method'] = request.method
            record.extra['path'] = request.path

        with mailhandler.contextbound(processor=inject_extra):
            # execute code that might fail in the context of the
            # request.

    $ easy_install Flask
    $ python hello.py
     * Running on http://localhost:5000/
"""
from setuptools import setup


setup(
    name='Logbook',
    version='0.1',
    license='BSD',
    long_description=__doc__,
    packages=['logbook'],
    zip_safe=False,
    platforms='any',
    test_suite='test_logbook'
)
