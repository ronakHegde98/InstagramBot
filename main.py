from InstaBot import InstaBot
import configparser
import re

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

  return conf

if __name__ == "__main__":
  config_file = "config.ini"
  config = parse_config(config_file)
  bot = insta_bot.InstaBot(config['credentials'], config['hashtags'], config['schedule'])
  bot.execute()


