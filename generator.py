from lxml import etree

root = etree.Element('ART')
artconfig = etree.SubElement(root, "artconfig")
mainPath = etree.SubElement(artconfig, "mainPath")
mainPath.text = "TEXT"
forecastMode = etree.SubElement(artconfig, "forecastMode")
forecastMode.text = "0"



print(etree.tostring(root, pretty_print=True))