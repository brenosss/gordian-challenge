import xml.etree.ElementTree as ET
import argparse
import json
import pprint

DEFAULT_FILE = 'OTA_AirSeatMapRS'


def save_result(result, path=f'{DEFAULT_FILE}.json'):
    with open(path, 'w') as f:
        f.write(json.dumps(result, indent=4, sort_keys=True))


def load_xml(path=f'{DEFAULT_FILE}.xml'):
    tree = ET.parse(path)
    namespaces = {'ns': 'http://www.opentravel.org/OTA/2003/05/common/'}
    return tree.getroot(), namespaces


def parser_seat_item(seat, full, extra_fields):
    x = {'Features': []}
    for item in seat:
        tag_without_ns = item.tag.partition('}')[-1]
        if tag_without_ns == 'Summary':
            x[tag_without_ns] = include_keys(item.attrib, full, extra_fields)
        elif tag_without_ns == 'Features':
            x[tag_without_ns].append(item.text)
        elif tag_without_ns == 'Status':
            x[tag_without_ns] = item.text
        elif tag_without_ns == 'Service':
            x['Price'] = item[0].attrib['Amount']
            x['CurrencyCode'] = item[0].attrib['CurrencyCode']
    return x


def include_keys(dictionary, full=False, extra_fields=[]):
    if full:
        return dictionary
    allowed_keys = [
        'CabinType',
        'Summary',
        'SeatNumber',
        'Price',
        'AvailableInd',
        'Rows',
        'Seats',
        'CurrencyCode',
    ]
    allowed_keys.extend(extra_fields)
    key_set = set(allowed_keys) & set(dictionary.keys())
    return {key: dictionary[key] for key in key_set}


def parser_seat_flat(full, extra_fields=[]):
    result = []
    root, namespaces = load_xml()
    cabins = root.findall('.//ns:CabinClass', namespaces=namespaces)
    for cabin in cabins:
        rows = cabin.findall('./ns:RowInfo', namespaces=namespaces)
        for row in rows:
            seats = row.findall('./ns:SeatInfo', namespaces=namespaces)
            for seat in seats:
                result.append(include_keys(
                    {
                        'Layout': cabin.attrib['Layout'],
                        'RowNumber': row.attrib['RowNumber'],
                        'CabinType': row.attrib['CabinType'],
                        **parser_seat_item(seat, full, extra_fields),
                        **seat.attrib
                    },
                    full=full,
                    extra_fields=extra_fields,
                ))
    return result

def parser_seat_normalized(full, extra_fields=[]):
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
                list_seats.append(
                    include_keys(
                        {
                            **parser_seat_item(seat, full, extra_fields),
                            **seat.attrib
                        },
                        full=full,
                        extra_fields=extra_fields
                    )
                )
            list_rows.append(include_keys(
                {
                    'RowNumber': row.attrib['RowNumber'],
                    'CabinType': row.attrib['CabinType'],
                    'Seats': list_seats
                },
                full=full,
                extra_fields=extra_fields
            ))
        result.append({
            'Layout': cabin.attrib['Layout'],
            'Rows': list_rows
        })
    return result

def extract_seats_data(args):
    if args.flat:
        result = parser_seat_flat(args.full, args.extra_fields)
    else:
        result = parser_seat_normalized(args.full, args.extra_fields)
    if args.output_file:
        save_result(result, path=args.output_file)
    else:
        save_result(result)
    if args.print:
        pprint.pprint(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flat",
        const=True,
        nargs='?',
        default=False,
        help='Export data in a flat format'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file name',
    )
    parser.add_argument(
        "--print",
        const=True,
        nargs='?',
        default=False,
        help='Print result on console'
    )
    parser.add_argument(
        "--full",
        const=True,
        nargs='?',
        default=False,
        help='Extract all fields'
    )
    parser.add_argument(
        '--extra-fields',
        nargs='*',
        type=str,
        default=[],
        help='Add extra fields to be extract, ex [ColumnNumber, ExitRowInd, PlaneSection, Status]'
    )
    args = parser.parse_args()
    extract_seats_data(args)


if __name__ == "__main__":
    main()
