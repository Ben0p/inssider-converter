import glob, os
import time
import csv
import kml


# Start timer
start_time = time.time()

# Get working directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# input files
input_path = '{}/input/'.format(dir_path)

# output files
output_path = '{}/output/'.format(dir_path)

# Create directories
if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(input_path):
    os.makedirs(input_path)
    input("Put .gpx files in the 'input' directory and press [Enter]: ")

# Change directory to input files folder
os.chdir(input_path)

# Get all files ending in .txt
for gpx_file in glob.glob("*.gpx"):
    print('Converting '+gpx_file)
    csv.convert(gpx_file)

# Change directory to output files folder
os.chdir(output_path)

for csv_file in glob.glob("*.csv"):
    print('Converting '+csv_file)
    kml.generate(csv_file)

elapsed = time.time() - start_time
print("Completed in {0:.2f} seconds".format(elapsed))
input("Press enter to exit ;)")