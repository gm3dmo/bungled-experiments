
import sys
import yaml
import string
import logging
import optparse
import BaseHTTPServer


class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        hostname = self.path[1:]
        logging.debug('access to: {0}'.format(self.path))
        logging.debug('xgenerating a kickstart for: {0}'.format(hostname))
        ks_template_file = 'ks.template'
        systems_yaml_file = 'systems.yaml'
        d = getsystems(systems_yaml_file)
        conf = generate_config(d, hostname)
        ks = ksgenerate(conf, ks_template_file)
        self.wfile.write("{}</body></html>".format(ks))


def generate_config(config, hostname):
        logging.debug('generate_config from :{0} for {1}'.format(config, hostname))
        host_config = {}
        logging.debug('ERK: {0}'.format(config['hosts'][hostname]['eth0']))
        if 'netmask' in config['hosts'][hostname]['eth0']:
            logging.debug('skipping host netmask its set on the host  {0}'.format(hostname))
            next
        else:
            logging.debug('hosts netmask set from default for:  {0}'.format(hostname))
        logging.debug('config for: {0} = {1}'.format(hostname, config['hosts'][hostname]))
        return config['hosts']


def getsystems(systems_yaml_file):
    try:
       with open(systems_yaml_file, 'r') as stream:
           definitions  = yaml.load(stream)
           logging.debug('system definitions from yaml: {0}'.format(definitions))
           return definitions
    except Exception, e:
       raise 


def cfgenerate(hostname):
    hosts = {}
    conf = hosts[hostname]
    return conf


def ksgenerate(conf, ks_template_file):
   logging.debug('ksgenerating a kickstart for: {0}'.format(type(conf)))
   logging.debug('ksgenerating with data: {0}'.format(conf))
   
   with open(ks_template_file, 'r') as f:
        t = string.Template(f.read())
        kickstart_file = t.safe_substitute(conf[0])

   return kickstart_file


def main():
    """Script to strain a set of variables through a kickstart file and serve them up royally"""

    LEVELS = { 'debug':logging.DEBUG,
               'info':logging.INFO,
               'warning':logging.WARNING,
               'error':logging.ERROR,
               'critical':logging.CRITICAL,
            }

    parser = optparse.OptionParser()
    parser.add_option('-p', '--port',
                      dest="listen_port",
                      default="8000",
                      type="int",
                      help='port the script will listen on for http request'
                      )
    parser.add_option('-l', '--logfile',
                      dest="logfile",
                      default="test.log",
                      help='sets the log file'
                      )
    parser.add_option('-t', '--templatefile',
                      dest="ks_template",
                      default="ks.template",
                      help='sets the log file'
                      )
    parser.add_option('-v', '--verbose',
                      dest="verbose",
                      default=False,
                      action="store_true",
                      help='Turn on debug messages to file (test.log).For when things get fruity!'
                      )
    parser.add_option('--version',
                      dest="version",
                      default=0.1,
                      type="float",
                      )

    options, remainder = parser.parse_args()

    if options.verbose == True:

       logger = logging.getLogger()

    
       logger.setLevel(logging.DEBUG)
       formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

       ch = logging.StreamHandler()

       logger.addHandler(ch)

                        
    else:
       pass

    try:
      options.help == True
      print_help()
      sys.exit(0)
    except:
       pass


    logging.debug('Starting xkickstart listener on port: ({0})'.format(options.listen_port))
    logging.debug('Using template file ({0})'.format(options.ks_template))

    BaseHTTPServer.HTTPServer(('', options.listen_port), MyHTTPRequestHandler).serve_forever()


if __name__ == '__main__':
    sys.exit(main())
