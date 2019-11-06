from datetime import datetime
import xml.etree.ElementTree

'''
Input .gpx 
Converts to formatted .csv
Returns filename of .csv
'''

def convert(file_in):
    '''
    Input .gpx file
    Output formatted .csv
    '''

    # File name excluding extention
    file_name = file_in.split('.')[0]
    # Formatted date YYYYmmdd
    timestamp = datetime.now().strftime('%Y%m%d')
    # Initialize .xml
    e = xml.etree.ElementTree.parse(file_in).getroot()
    # Master Dictionary
    master = {}

    # SSID list
    ssid_list = []
    

    # Read each waypoint
    for count, waypoint in enumerate(e.findall('wpt')):

        latlon = waypoint.attrib
        
        dtime = waypoint.find('time').text
        rept = dtime.replace('T', ' ')

        extensions = waypoint.find('extensions')

        ssid = extensions.find('SSID').text

        if ssid not in ssid_list:
            ssid_list.append(ssid)
            master[ssid] = []


        master[ssid].append(
            {
                'lat' : latlon['lat'],
                'lon' : latlon['lon'],
                'time' : rept.replace('Z', ' '),
                'ele' : waypoint.find('ele').text,
                'sats' : waypoint.find('sat').text,
                'hdop' : waypoint.find('hdop').text,
                'vdop' : waypoint.find('vdop').text,
                'pdop' : waypoint.find('pdop').text,
                'ssid' : extensions.find('SSID').text,
                'mac' : extensions.find('MAC').text,
                'rssi' : extensions.find('RSSI').text,
                'qual' : extensions.find('signalQuality').text,
                'chan' : extensions.find('ChannelID').text,
                'priv' : extensions.find('privacy').text,
                'typ' : extensions.find('networkType').text,
                'rates' : extensions.find('rates').text
            }
        )

    
    for network in ssid_list:
        file_out = '../output/{}-{}-{}.csv'.format(timestamp, file_name, network)
        print('Generating {}'.format(file_out))

        with open(file_out, 'w') as fo:
            # Add Headers
            fo.write('time,ssid,mac,latitude,longitude,elevation,rssi,quality,channel,sats,hdop,vdop,pdop,privacy,type,rates\n')

            for point in master[network]:
                fo.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                    point['time'],
                    point['ssid'],
                    point['mac'],
                    point['lat'],
                    point['lon'],
                    point['ele'],
                    point['rssi'],
                    point['qual'],
                    point['chan'],
                    point['sats'],
                    point['hdop'],
                    point['vdop'],
                    point['pdop'],
                    point['priv'],
                    point['typ'],
                    point['rates']
                ))




if __name__ == '__main__':
    file_in = 'input/west.gpx'
    convert(file_in)