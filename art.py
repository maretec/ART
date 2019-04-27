import xml.etree.ElementTree as ET

root = ET.parse('file.xml').getroot()

def searchTag(attributePath):
  return root.find(attributePath)

print(root.find("./config/artconfig/mainPath").text)