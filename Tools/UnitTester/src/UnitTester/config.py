from .constants.Commands import Commands
from .constants.ConfigKeys import ConfigKeys
from .constants.EnvironmentModes import EnvironmentModes


# Configurations for the program are used as a global variable to
#   allow passing of configuration to the integration tests
Config = {ConfigKeys.Command: Commands.RunSuite,
          ConfigKeys.DbTool: None,
          ConfigKeys.DbCleaner: None,
          ConfigKeys.EnvironmentMode: EnvironmentModes.Dev}
