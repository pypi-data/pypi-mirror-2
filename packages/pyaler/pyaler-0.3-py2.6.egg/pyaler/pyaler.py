#! /usr/bin/python
# -*- coding: utf-8 -*-

##################################################
# Pyaler is a script aimed to give a REST interface
# giving several Arduinos modules through their serial
# interface from Internet.
#
# This application depends on the following libraries:
#  - bottle -> http://bottle.paws.de/ (bundled with this code)
#  - PyYaml -> http://pyyaml.org/wiki/PyYAML
#  - PySerial -> http://pyserial.sourceforge.net/
#
# Copyleft (C) 2010 Bernard `Guyzmo` Pratz [Bearstech]
# Copyleft (C) 2010 Lucas Fernandez [Bearstech]
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License v2
# as published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# <http://www.gnu.org/licenses/gpl-2.0.html>.
##################################################

##################################################
# example arduino code :
##################################################
# int incomingByte = 0;
# void setup() {
#       Serial.begin(9600);
# }
#
# void loop() {
#   if (Serial.available() > 0) {
#               incomingByte = Serial.read();
#
#               Serial.print("I received: ");
#               Serial.println(incomingByte, DEC);
#       }
# }
##################################################

##################################################
# example configuration file (working for OSX with the above code) :
##################################################
# arduinos:
#     arduino1: /dev/tty.usbserial-A800eIR3
#     arduino2: /dev/tty.usbserial-A800eIho
#
# read_actions:
#     read:
#
# write_actions:
#     write:
##################################################

import sys
import logging as log
import serial, yaml
from bottle import Bottle, route, run, request
from optparse import OptionParser

app = Bottle()

arduinos = {}
read_actions = {}
write_actions = {}

# create serial connections to connect to the arduinos
arduicon = {}

def arduino_write(ard, val):
    """
    function used to write on an arduino

    @param ard name of the arduino as given in the configuration file
    @param val value to send to the arduino
    """
    ser = arduicon[ard]
    log.debug('written into arduino: %s %s byte(s)', ard, ser.write('%s' % val))
    return 'OK'

def arduino_read(ard):
    """
    function used to read from an arduino

    @param ard name of the arduino as given in the configuration file
    """
    ser = arduicon[ard]
    log.debug('reading from arduino: %s', ard)
    return ser.readlines()

@app.route('/arduinos/reset')
def arduinos_reset():
    """
    function to reload connections to arduinos
    """
    # retrieve arduinos configuration and actions from config file
    arduinos.clear()
    read_actions.clear()
    write_actions.clear()

    try:
        config_file = request.environ['pyaler.config']
        config = yaml.load(file(config_file, 'r'))

        arduinos.update(config['arduinos'])
        read_actions.update(config['read_actions'])
        write_actions.update(config['write_actions'])
    except yaml.YAMLError, exc:
        log.error("Error in configuration file: %s", exc)
        return 'ERROR'
    else:
        log.info("%s loaded", config_file)

    log.info("Updated arduinos and actions from configuration file.")

    arduicon.clear()
    for arduino in arduinos:
        try:
            s = serial.Serial(arduinos[arduino], baudrate=9600, timeout=2)
            arduicon[arduino] = s
        except Exception, ex:
            log.warn("Couldn't connect to arduino: %s having chardev %s", arduino, arduinos[arduino])
    return 'OK'

@app.route('/get/:arduino/:action')
def arduino_action_getter(arduino, action):
    """
    function to get a value from the arduino, given an action

    @param arduino name of the arduino binding given in the configuration file
    @param action name of the action to do on the arduino (will be checked against read_actions dict's
                  keys and send the matching message to the arduino)
    """
    if arduino in arduicon:
        if action in read_actions:
            if not read_actions[action] is None:
                arduino_write(arduino, read_actions[action])
            return arduino_read(arduino)
        else:
            return 'action is not existent.<br />Please choose one from : '+", ".join(read_actions.keys())+"<br />\n"
    else:
        return 'arduino is not existent.<br /> Please choose one from : '+", ".join(arduicon.keys())+"<br />\n"

@app.route('/set/:arduino/:action', method='POST')
def arduino_action_setter(arduino, action):
    """
    function to get a value on the arduino, given an action

    @param arduino name of the arduino binding given in the configuration file
    @param action name of the action to send to the arduino (will be checked against write_actions dict's
                  keys and send to the arduino the matching message followed by the 'value' POST parameter)

    that method needs a POST parameter 'value' set to the value you want to set on the pin.
    """
    if arduino in arduicon:
        if action in write_actions:
            if 'value' in request.POST:
                value = request.POST['value']
                arduino_write(arduino, (write_actions[action] or '')+value)
                return 'OK'
            else:
                return 'missing expected POST element called "value".<br />\n'
        else:
            return 'action is not existent.<br />Please choose one from : '+", ".join(write_actions.keys())+"<br />\n"
    else:
        return 'arduino is not existent.<br /> Please choose one from : '+", ".join(arduicon.keys())+"<br />\n"

class App(object):

    def __init__(self, app, config, **kwargs):
        self.app = app
        self.config = config
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        environ['pyaler.config'] = self.config
        environ['pyaler.app_config'] = self.kwargs
        return self.app(environ, start_response)

def make_app(global_conf, **local_conf):
    if 'app' in local_conf:
        app_module = local_conf['app']
        del local_conf['app']
        __import__(app_module, globals(), locals(), [''])
    pyaler_app = App(app, **local_conf)
    def start_response(*args, **kwargs): pass
    environ = {'PATH_INFO': '/arduinos/reset'}
    pyaler_app(environ, start_response)
    return pyaler_app

def main(config=None):

    parser = OptionParser(usage="%prog -v -H HOST -p PORT -c file", version="pyaler v0.3")
    parser.add_option("-H", "--host", dest="host", default='localhost',
            help="Host to run the pyaler server as. Default: localhost", metavar="HOST")
    parser.add_option("-p", "--port", dest="port", default='8080',
            help="Port where run the pyaler server on. Default: 8080", metavar="PORT")
    parser.add_option("-c", "--conf", default=config or 'conf.yaml',
                    action="store", type="string", dest="config", metavar="CONFIG",
                    help="Path to configuration file. Default: conf.yaml")
    parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="Print logging messages to stdout.")


    (options, args) = parser.parse_args()

    if options and options.verbose: level=log.DEBUG
    else:                           level=log.ERROR

    log.basicConfig(stream=sys.stdout, level=level)
    run(app=make_app({}, config=options.config), host=options.host, port=int(options.port))

if __name__ == '__main__':
    config = '../conf.yaml'
    main(config=config)


