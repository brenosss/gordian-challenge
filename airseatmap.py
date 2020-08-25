import xml.etree.ElementTree as ET
import json


def parser_seat_item(seat):
    x = {'Features': []}
    for item in seat:
        tag_without_ns = item.tag.partition('}')[-1]
        if tag_without_ns == 'Summary':
            x[tag_without_ns] = item.attrib
        elif tag_without_ns == 'Features':
            x[tag_without_ns].append(item.text)
        elif tag_without_ns == 'Status':
            x[tag_without_ns] = item.text
        elif tag_without_ns == 'Service':
            x[tag_without_ns] = item[0].attrib['Amount']
    return x


def parsr_air_seats():
    result = []
    tree = ET.parse('OTA_AirSeatMapRS.xml')
    root = tree.getroot()
    namespaces = {'ns': 'http://www.opentravel.org/OTA/2003/05/common/'}
    cabins = root.findall('.//ns:CabinClass', namespaces=namespaces)
    for cabin in cabins:
        rows = cabin.findall('./ns:RowInfo', namespaces=namespaces)
        for row in rows:
            seats = row.findall('./ns:SeatInfo', namespaces=namespaces)
            for seat in seats:
                x = {}
                result.append({
                    'Layout': cabin.attrib['Layout'],
                    'RowNumber': row.attrib['RowNumber'],
                    'CabinType': row.attrib['CabinType'],
                    **parser_seat_item(seat),
                    **seat.attrib
                })
    return result

result = parsr_air_seats()
