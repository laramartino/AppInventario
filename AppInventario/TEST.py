import configparser

config = configparser.ConfigParser()

config.add_section('EXPORT')

config.set('EXPORT', 'destination', 'C:/Users/Lara/Desktop')

with open ('export.ini', 'w') as f:
    config.write(f)