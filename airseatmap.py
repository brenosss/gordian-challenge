import xml.etree.ElementTree as ET
import argparse
import json


def load_xml(path='OTA_AirSeatMapRS.xml'):
    tree = ET.parse('OTA_AirSeatMapRS.xml')
    namespaces = {'ns': 'http://www.opentravel.org/OTA/2003/05/common/'}
    return tree.getroot(), namespaces


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


def parser_seat_planned():
    result = []
    root, namespaces = load_xml()
    cabins = root.findall('.//ns:CabinClass', namespaces=namespaces)
    for cabin in cabins:
        rows = cabin.findall('./ns:RowInfo', namespaces=namespaces)
        for row in rows:
            seats = row.findall('./ns:SeatInfo', namespaces=namespaces)
            for seat in seats:
                result.append({
                    'Layout': cabin.attrib['Layout'],
                    'RowNumber': row.attrib['RowNumber'],
                    'CabinType': row.attrib['CabinType'],
                    **parser_seat_item(seat),
                    **seat.attrib
                })
    return result

def parser_seat_normalized():
    result = []
    root, namespaces = load_xml()
    cabins = root.findall('.//ns:CabinClass', namespaces=namespaces)
    for cabin in cabins:
        rows = cabin.findall('./ns:RowInfo', namespaces=namespaces)
        list_rows = []
        for row in rows:
            seats = row.findall('./ns:SeatInfo', namespaces=namespaces)
            list_seats = []
            for seat in seats:
                list_seats.append({
                    **parser_seat_item(seat),
                    **seat.attrib
                })
            list_rows.append({
                'RowNumber': row.attrib['RowNumber'],
                'CabinType': row.attrib['CabinType'],
                'Seats': list_seats
            })
        result.append({
            'Layout': cabin.attrib['Layout'],
            'Rows': list_rows
        })
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--format',
        type=str,
        help='Output JSON format',
        choices=['normalized', 'planned'],
        default='normalized')
    args = parser.parse_args()
    if args.format == 'planned':
        result = parser_seat_planned()
    elif args.format == 'normalized':
        result = parser_seat_normalized()

if __name__ == "__main__":
    main()
