import configparser

config = configparser.ConfigParser()

config.read("config.cfg")

print(config['Database']['path'])
