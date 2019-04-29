import yaml

with open("file.yaml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

for section in cfg:
  print(cfg[section])
