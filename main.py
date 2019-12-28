from InstaBot import InstaBot
import configparser
import re
import socket

def parse_config(config_file):
  """Parse configuration file provided by user"""

  conf = {}
  config = configparser.ConfigParser()
  valid_schedule = r'\d{1,2}:\d{2}(:\d{2})*\s+[AM|PM]'
  
  #configparser does not throw exception (empty dataset if files are not found)
  if(len(config.read(config_file)) == 0):
    raise FileNotFoundError("Failed to find config file")


  conf['credentials'] = {"username": config['credentials']['username'], "password": config['credentials']['password']}
  conf['hashtags'] = [hashtag for hashtag in config['hashtags'].values()]
  conf['schedule'] = [time.upper() for time in config['schedule'].values() if re.search(valid_schedule,time, re.IGNORECASE)]
  conf['driverpath'] = config['driver']['path']

  return conf

def is_connected():
  """Quickly check internet connection """
  
  try:
      socket.create_connection(("www.google.com", 80))
      return True
  except OSError:
      pass
  return False


if __name__ == "__main__":
  if(is_connected()):
    config_file = "config.ini"
    config = parse_config(config_file)
    bot = InstaBot(config)
    bot.execute()
  else:
    print('Please check internet connectivity')

