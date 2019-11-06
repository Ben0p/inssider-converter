import os


'''
Mine Systems cisco drive csv to kml converter
Input a formatted .csv of the cisco-drive results
Generates a .kml
'''


def generate(csv_in):
    '''
    Generate a .kml from a formatted .csv
    csv_in is the input formatted .csv
    '''

    # Header of .kml
    header = (
        '<?xml version="1.0" encoding="utf-8" ?>'
        '<kml xmlns="http://www.opengis.net/kml/2.2">'
        '   <Document id="root_doc">'
    )

    # Ledgend of the colors for each throughput result
    ledgend = (
        '       <Folder><name>Legend - RSSI</name>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#ace600;&quot;&gt;&lt;b&gt;Greater than -50dBm&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#00e674;&quot;&gt;&lt;b&gt;-60dBm&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#003ae6;&quot;&gt;&lt;b&gt;-70dBm&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#e600e6;&quot;&gt;&lt;b&gt;-80dBm&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:#e60000;&quot;&gt;&lt;b&gt;Less than -80dBm&lt;/b&gt;&lt;/span&gt;</name>'
        '           </Placemark>'
        '       </Folder>'
    )
    
    # Name for the drive results folder
    name = (
        '       <Folder><name>Track - {}</name>'
    )

    # Placemark for each segment of the results
    placemark = (
        '           <Placemark>'
        '               <name>&lt;span style=&quot;color:{c}&quot;&gt;{r}: {rssi}dBm&lt;/span&gt;</name>'
        '               <Style><LineStyle><color>{lc}</color><width>4</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>'
        '               <LineString><coordinates>{lon1},{lat1} {lon2},{lat2}</coordinates></LineString>'
        '           </Placemark>'
    )

    # Closing out the .kml
    footer = (
        '       </Folder>'
        '   </Document>'
        '  </kml>'
    )

    # Colors for throughputs
    color = {
        '4':'#e60000',
        '3':'#e600e6',
        '2':'#003ae6',
        '1':'#00e674',
        '0':'#ace600'
        }

    # Colors for the segments
    line_color = {
        '4':'ff0000e6',
        '3':'ffe600e6',
        '2':'ffe63a00',
        '1':'ff748600',
        '0':'ff00e6ac'
        }


    # Get the filename only from absolute directory?
    csv_filename = os.path.basename(csv_in)
    # Get the filename without extension
    drive_name = os.path.splitext(csv_filename)[0]
    # Add .kml extension to the drive_name
    kml_name = drive_name+'.kml'

    # Start point counter
    count = 0

    # Create .kml file
    with open(kml_name, 'w') as kml:
        # Write the header and ledgend to file
        kml.write(header)
        kml.write(ledgend)
        # Set the name inside kml
        name = name.format(drive_name)
        kml.write(name)

        # Open csv file for read only
        with open(csv_in,'r') as f:
            # Read each line
            for row in f:
                # Split line with comma deliminator
                cell = row.split(',')
                
                # Skip the first line in csv containing header info
                if count == 0:
                    count += 1
                    continue

                # Generate start of first segment from first point
                if count == 1:
                    lat2 = cell[3]
                    lon2 = cell[4]
                # From second point onwards, start of segment is the end of last segment
                else:
                    lat2 = lat1
                    lon2 = lon1
                # Second point of segment
                lat1 = cell[3]
                lon1 = cell[4]
                
                # Convert rssi to float
                rssi = float(cell[6])
                
                # Set segment colors based on upload connection rate
                if rssi >= -50:
                    rc = color['0']
                    lc = line_color['0']
                elif -60 <= rssi < -50:
                    rc = color['1']
                    lc = line_color['1']
                elif -70 <= rssi < -60:
                    rc = color['2']
                    lc = line_color['2']
                elif -80 <= rssi < -70:
                    rc = color['3']
                    lc = line_color['3']
                elif rssi < -80:
                    rc = color['4']
                    lc = line_color['4']
                

                # Insert values into the kml segment
                track = placemark.format(
                    c=rc,
                    r=count,
                    rssi=rssi,
                    lon1=lon1,
                    lat1=lat1,
                    lon2=lon2,
                    lat2=lat2,
                    lc=lc
                    )

                # Write segment to file      
                kml.write(track)
                # Increase count
                count += 1
            # Print total points
            print("Processed {} points".format(count))
            # Close csv file
            f.close
        # Write out the footer to kml
        kml.write(footer)
        # Close the kml
        kml.close



if __name__ == '__main__':
    csv_file = '20180914-CTO-BRA.csv'
    generate(csv_file)