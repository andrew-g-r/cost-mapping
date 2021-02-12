import numpy as np
import json
from pathlib import Path
import googlemaps

#googlemaps api key
gmaps = googlemaps.Client(key='AIzaSyBqERDKGUinc-sQi_IO9G1bCIRtxUyz4bU', timeout=.5)

#directories
file_dir = '/data/limited_grid/'
data_dir = '/data/'

#bounds of our grid 
xbounds1 = 29.979508
xbounds2 = 30.660661
ybounds1 = -97.980544
ybounds2 = -97.299391

#Trips from and back to this location
current_coordinates = [30.300501, -97.748948]

#space between points
xwidth = abs(xbounds1-xbounds2)/16
ywidth = abs(ybounds1-ybounds2)/16
#space between the interpolated points
xwidth_fine = abs(xbounds1-xbounds2)/48
ywidth_fine = abs(ybounds1-ybounds2)/48

#create numpy arrays
x = np.arange(xbounds1, xbounds2, xwidth)
y = np.arange(ybounds1, ybounds2, ywidth)

x_fine = np.arange(xbounds1, xbounds2, xwidth_fine)
y_fine = np.arange(ybounds1, ybounds2, ywidth_fine)

#the original meshgrid
X,Y = np.meshgrid(x,y)

#with this information we can start creating requests for google maps
#create an array of grid points
gridpoints = []
for i in range(16):
    for p in range(16):
        gridpoints.append([x[p], y[i]])
#the jumps or trips for the data
grid_jumps = []            
for i in gridpoints:
    grid_jumps.append((current_coordinates, i, current_coordinates))
#save a file for later use
with open(data_dir+'limited_grid_coordinate_data.json', 'w') as outfile:
            json.dump(grid_jumps, outfile)

#begin making requests as needed
for i in grid_jumps:
    starting_location = i[0]
    intermediate_coordinates = [i[1]]
    ending_location = i[0]
    filename = str(i[1]).replace(', ', '_').strip('[]')
    file_path = Path(filename + '_results.json')
    if (file_path).is_file():
        with open(file_dir + filename + '_results.json', encoding="utf8") as f:
            results = json.load(f)
            print('loaded file:\n{}'.format(file_dir + filename + '_results.json'))
    else:
        results = gmaps.directions(
            origin=starting_location,
            destination=ending_location,
            waypoints=intermediate_coordinates,
            avoid='tolls')
        with open(file_dir + filename + '_results.json', 'w') as outfile:
            json.dump(results, outfile)
        print('created file:\n{}'.format(file_dir + filename + '_results.json'))
    #do not make requests as fast as programmatically possible
    time.sleep(1)            

#pulling the requests data to populate the data for the Z axis
for i in gridpoints:
    latitude = i[0]
    longitude = i[1]
    indexX = np.where(X == latitude)[1][0]
    indexY = np.where(Y == longitude)[0][0]
    target_name = latitude, longitude
    target_name = str(target_name).replace(', ', '_').strip('()')

    with open(target_name + '_results.json', encoding="utf8") as f:
        results = json.load(f)
    for p in results[0]['legs']:

        distance = (p['distance']['value']/1609.34)
        duration = (p['duration']['value']/60)

    Z[indexY][indexX] = distance
    
with open(data_dir+'Z_array.json', 'w') as outfile:
        json.dump(Z, outfile)