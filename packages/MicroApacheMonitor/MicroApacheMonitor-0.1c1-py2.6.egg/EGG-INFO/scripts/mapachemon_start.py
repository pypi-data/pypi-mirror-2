from mapachemon.mapachemon import *

def main():
    icon = resource_filename('mapachemon', 'mapachemon.ico')
    
    usage = 'usage: %prog [options] serverpath'
    parser = OptionParser(usage=usage)
    parser.set_defaults(show_window=False, autostart=True)
    parser.add_option('-m', '--manual-start', dest='autostart',
                      action='store_false', help=('Don''t autostart (default '
                                                  'is to autostart)'))
    parser.add_option('-l', '--logfile', dest='logfile', action='store',
                      type='string', help=('log errors to LOGFILE (default is '
                                           'mapachemon.log in the server '
                                           'directory)'))
    parser.add_option('-s', dest='show_window', action='store_true',
                      help=('show the command window (default is to hide the '
                            'command window)'))
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        return
    elif len(args) > 1:
        parser.error('Too many positional arguments specified! You may need ' +
                     'to put quotes around the serverpath argument.')
    server = os.path.abspath(args[0])
    logfile = options.logfile or os.path.join(os.path.split(server)[0], 'mapachemon.log')
    m = MicroApache(server, logfile)
    if options.autostart:
        m.start()
    if not options.show_window:
        hideConsole()
    def start(sysTrayIcon): m.start()
    def stop(sysTrayIcon): m.stop()
    def restart(sysTrayIcon): m.restart()
    def quit(sysTrayIcon):
        m.stop()
        showConsole()
    menu_options = (('Start', None, start),
                    ('Stop', None, stop),
                    ('Restart', None, restart)
                    )
    SysTrayIcon(icon, hover_text='MicroApache Monitor',
                menu_options=menu_options, on_quit=quit)

if __name__ == '__main__':
    main()
    
