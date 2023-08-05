#
#  Deals with configuration data
#

import ConfigParser
import StringIO

# The default configuration
default_cfg = StringIO.StringIO("""
[main]
listeners = tcp
debug = false

[tcp]
type = tcp
port = 8099
interface = localhost
""")

# The configuration object
config = ConfigParser.SafeConfigParser()
config.readfp(default_cfg)
