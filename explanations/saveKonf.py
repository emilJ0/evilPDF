from configparser import ConfigParser

configFile = ConfigParser()
configFile.read("explanations/test.ini")

print(configFile["sektion"]["var"]) # Output: Wert

configFile["sektion"]["var"] = "neuerWert"
print(configFile["sektion"]["var"]) # Output: neuerWert

with open('test.ini', 'w') as configfile:
    configFile.write(configfile)
