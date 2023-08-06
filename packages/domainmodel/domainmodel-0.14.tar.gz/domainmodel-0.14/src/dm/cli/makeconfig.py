import os
import sys

class DomainConfigMaker(object):

    template = ''

    usage  = '''usage: %prog [path]

Generate new configuration file from template, see --help for options.

Writes file to path if given, otherwise prints to stdout.
        '''

    def __init__(self, systemName):
        self.systemName = systemName
        # Define input options.    
        from optparse import OptionParser
        parser = OptionParser(self.usage)
        self.addOptions(parser)
        # Parse input arguments.
        (options, args) = parser.parse_args()
        if len(args) > 1:
            print 'Error: You have supplied too many arguments.\n'
            parser.print_help()
            sys.exit(1)
        elif args:
            configPath = args[0]
        else:
            configPath = None
        # Define configuration argument.
        optionLines = []
        self.addOptionLines(options, optionLines)
        # Make configuration line.
        configLines = self.makeLines(optionLines)
        # Output configuration lines.
        if configPath:
            configFile = file(configPath, 'w')
            configFile.writelines(configLines)
            configFile.close()
        else:
            print "".join(configLines)

    def addOptions(self, parser):
        parser.add_option(
            '--master-dir',
            dest='masterDir',
            #default='/path/to/%s' % self.systemName,
            help="""The path to the folder for service files.""")

        parser.add_option(
            '--service-name',
            dest='serviceName',
            help='The service name to be used.')

        parser.add_option(
            '--system-mode',
            dest='systemMode',
            help='The mode of the system (production or development).')

        parser.add_option(
            '--password-digest-secret',
            dest='passwordDigestSecret',
            help='The "secret" used as "salt" for password digests. Use the old system value when upgrading.')

        parser.add_option(
            '--environment-timezone',
            dest='environmentTimezone',
            help='The timezone to be used.')

        parser.add_option(
            '--domain-name',
            dest='domainName',
            help="""The fully qualified domain name where the site will be served.""")

        parser.add_option(
            '--db-type',
            dest='dbType',
            help="""The database type to be used. The choices are 'sqlite',
'postgres' or 'mysql'. The default is 'sqlite'.""")

        parser.add_option(
            '--db-name',
            dest='dbName',
            help='The name of the database instance.')

        parser.add_option(
            '--db-user',
            dest='dbUser',
            help='The database user to be used for reading and updating the database.')

        parser.add_option(
            '--db-pass',
            dest='dbPass',
            help='The database password to be used for reading and updating the database.')

        parser.add_option(
            '--db-super-user',
            dest='dbSuperUser',
            help='The database user to be used for creating and deleting databases.')

        parser.add_option(
            '--db-super-pass',
            dest='dbSuperPass',
            help='The database password to be used for creating and deleting databases.')

        parser.add_option(
            '--db-host',
            dest='dbHost',
            help='The database host to be used.')

        parser.add_option(
            '--virtualenv-bin-dir',
            dest='virtualenvBinDir',
            help='The virtual environment scripts folder.')

        parser.add_option(
            '--enable-memoization',
            dest='enableMemoization',
            action='store_true', 
            help='Enable memoization in the access controller.')

        parser.add_option(
            '--log-file',
            dest='logFile',
            help='The path to the log file.')

        parser.add_option(
            '--apache-config-file',
            dest='apacheConfigFile',
            help='The path to the auto-generated Apache config file.')

        parser.add_option(
            '--templates-dir',
            dest='templatesDir',
            help='Path to folder of HTML templates files.')

        parser.add_option(
            '--media-dir',
            dest='mediaDir',
            help='Path to folder of static media.')

        parser.add_option(
            '--wsgi-file',
            dest='wsgiFile',
            help='Path to the auto-generated WSGI file.')

        parser.add_option(
            '--email-enable-sending',
            dest='emailEnableSending',
            help="""Set this value to enable sending of email""")

        parser.add_option(
            '--email-notify-changes',
            dest='emailNotifyChanges',
            help="""Set this value to enable sending of notifications of changes to administrators""")
    
        parser.add_option(
            '--email-service-address',
            dest='emailServiceAddress',
            help="""The email address from which email will appear to have been sent""")

        parser.add_option(
            '--email-smtp-host',
            dest='emailSmtpHost',
            help="""The host to which SMTP connections will be made when sending email""")
    
    def addOptionLines(self, options, optionLines):
        optionLines.append('[DEFAULT]')
        if options.masterDir:
            absMasterDir = os.path.abspath(options.masterDir)
            optionLines.append('master_dir = %s' % absMasterDir) 
        if options.serviceName:
            optionLines.append('service_name = %s' % options.serviceName)
        if options.systemMode:
            optionLines.append('system_mode = %s' % options.systemMode)
        if options.domainName:
            optionLines.append('domain_name = %s' % options.domainName)
        optionLines.append('password_digest_secret = %s' % (options.passwordDigestSecret or self.generateNewSecretKey()))
        if options.environmentTimezone:
            optionLines.append('[environment]')
            optionLines.append('timezone = %s' % options.environmentTimezone)
        if options.virtualenvBinDir:
            optionLines.append('[virtualenv]')
            optionLines.append('bin_dir = %s' % options.virtualenvBinDir)
        optionLines.append('[db]')
        if not options.dbType:
            if options.dbName or options.dbPass or options.dbHost:
                options.dbType = 'postgres'
            # Don't set this, so that the value remain uncommented in the config file.
            #else:
            #    options.dbType = 'sqlite'
        if options.dbType in ['sqlite', None]:
            if not options.dbName:
                # Don't set this, so that the value remain uncommented in the config file.
                #options.dbName = '%(master_dir)s/var/sqlite.db'
                pass
        elif options.dbType in ['mysql', 'postgres']:
            msg = "Error: No database %%s (required for %s databases)." % options.dbType
            if not options.dbName:
                print msg % 'name'
                sys.exit(1)
            if not options.dbUser:
                print msg % 'user'
                sys.exit(1)
            if not options.dbPass:
                print msg % 'pass'
                sys.exit(1)
        if options.dbType:
            optionLines.append('type = %s' % options.dbType)
        if options.dbName:
            optionLines.append('name = %s' % options.dbName)
        if options.dbType in ['mysql', 'postgres']:
            if options.dbUser:
                optionLines.append('user = %s' % options.dbUser)
            if options.dbPass:
                optionLines.append('pass = %s' % options.dbPass)
            if options.dbSuperUser:
                optionLines.append('super_user = %s' % options.dbSuperUser)
            if options.dbSuperPass:
                optionLines.append('super_pass = %s' % options.dbSuperPass)
            if options.dbHost:
                optionLines.append('host = %s' % options.dbHost)
        if options.enableMemoization and options.systemMode != 'development':
            optionLines.append('[memos]')
            optionLines.append('enabled = on')
        optionLines.append('[django]')
        optionLines.append('secret_key = %s' % self.generateNewSecretKey())
        if options.templatesDir:
            optionLines.append('templates_dir = %s' % options.templatesDir)
        if options.logFile:
            optionLines.append('[logging]')
            optionLines.append('log_file = %s' % options.logFile)
        if options.apacheConfigFile or options.mediaDir or options.wsgiFile:
            optionLines.append('[www]')
            if options.apacheConfigFile:
                optionLines.append('apache_config_file = %s' % options.apacheConfigFile)
            if options.mediaDir:
                optionLines.append('media_dir = %s' % options.mediaDir)
            if options.wsgiFile:
                optionLines.append('wsgi_file = %s' % options.wsgiFile)
        optionLines.append('[email]')
        if options.emailEnableSending:
            optionLines.append('enable_sending = on')
        if options.emailNotifyChanges:
            optionLines.append('notify_changes = on')
        if options.emailServiceAddress:
            optionLines.append('service_address = %s' % options.emailServiceAddress)
        if options.emailSmtpHost:
            optionLines.append('smtp_host = %s' % options.emailSmtpHost)

        
    def generateNewSecretKey(self):
        import string
        from random import choice
        characters = string.letters + string.digits #+ string.punctuation
        return ''.join([choice(characters) for i in range(65)])

    def makeLines(self, optionLines):
        templateLines = self.template.split('\n')
        from dm.configwriter import ConfigWriter 
        configWriter = ConfigWriter()
        configWriter.updateLines(templateLines, optionLines)
        return configWriter.newLines
 
