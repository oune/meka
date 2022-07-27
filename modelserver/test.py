import configparser
import os
config = configparser.ConfigParser()

config['model'] = {'batchSize': '512',
                   'modelPath': '../model/',
                   'motorModelFileName': 'motor.pkl',
                   'pumpModelFileName': 'pump.pkl'}

# with open('config.ini', 'w') as configfile:
#     config.write(configfile)

a = os.path.join(config['model']['modelPath'],
                 config['model']['motorModelFileName'])
print(a)
