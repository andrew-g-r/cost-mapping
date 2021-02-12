# cost-mapping
Determining the cost and topology of transportation from a given point

The Ultimate goal is to create a web application that can provide useful cost data to the user.  The project originated as a way to analyze the cost of travel for gig workers on any given ‘gig’.  The real cost of these trips is often undervalued.  

Once we have some data, Matplotlib allows us to plot our cost data to a graph that somewhat resembles a gravity well more than a regular map.  The highpoints represent greater cost, and the low points represent the least cost.  The axis correspond to latitude and longitude of a geographic area.  The further from center the more expensive any trip grows, but obstacles like winding roads and indirect routes show up as hills or even mountains.

<p align="left">
  <img src="https://user-images.githubusercontent.com/77086418/107602022-f5c9db00-6bed-11eb-8a34-7faa7cfbf92f.png" width="250" height="200">
  <img src="https://user-images.githubusercontent.com/77086418/107601843-68868680-6bed-11eb-8d66-60fe1959dc24.gif" width="290" height="200">
</p>

To start we need information and the ability to determine travel time from one point to another, and not as the crow flies.  To that end we need some tools.

Googlemaps or another api like mapbox can provide this information in real time.

---

## Googlemaps Legs

```javascript
import googlemaps
import json

#using our googlemaps API key
gmaps = googlemaps.Client(key='AIzaSyBqERDKGUinc-sQi_IO9G1bCIRtxUyz4bU')

current_coordinates = [30.300501, -97.748948]
address_coordinates = []
intermediate_coodrinates = [
    [30.311987, -97.728008],
    ]

for address in delivery_locations:
    address_coordinates.append(address)
```
We can fire off a request and receive some data about our trip in json. It's a round trip starting at our current_coordinates and returning to them.
```Python
results = gmaps.directions(
    origin=current_coordinates,
    destination=current_coordinates,
    waypoints=intermediate_coodrinates
    )
 ```
The results file provide a wealth of data, but we're just interested in duration and distance right now.
```Python
for branch in results[0]['legs']:
    distance = branch['distance']['text']
    dururation = branch['duration']['text']
    total_distance += branch['distance']['value']
    total_duration += branch['duration']['value']
```

---

So we've garnered some information.  And we could fire off one of these requests as needed.  These services are not free and for what we have in mind we'd be making many thousands of these requests all the time.  In an ideal situation would go this route, as we get real time traffic data and we are not reinventing the google maps wheel.  We could use a bit less information, and still make educated costs about travel.  So we'll be making an interpolated model of the map using interp2d.

## Caching our results

```Python
with open('Resultsfile.json', 'w') as outfile:
    json.dump(results, outfile)
```

With enough of these requests we can make a pretty complete map of a given area, and the cost of each trip.

To start, we will create a lower resolution grid of all these points.  The finer the grid mesh, the more requests that would be required, so we settle for a 16x16 grid.  We are going to make room for interpolating that grid, and making some educated guesses about points between our 16x16, with an additional 48x48 points later.  The increase from 16x16 to 48x48 is arbitrary.  It could be 50x50 or 100x100, but the finer the grid, the less accurate the model will be.

```Python
xbounds1 = 30.169352
xbounds2 = 30.759423
ybounds1 = -98.027175
ybounds2 = -97.346022

xwidth = abs(xbounds1-xbounds2)/16
ywidth = abs(ybounds1-ybounds2)/16

xwidth_fine = abs(xbounds1-xbounds2)/48
ywidth_fine = abs(ybounds1-ybounds2)/48

x = np.arange(xbounds1, xbounds2, xwidth)
y = np.arange(ybounds1, ybounds2, ywidth)

x_fine = np.arange(xbounds1, xbounds2, xwidth_fine)
y_fine = np.arange(ybounds1, ybounds2, ywidth_fine)

```

## Interpolating and modeling our data
Enter numpy meshgrids, matplotlib, and interp2d.

```Python
X,Y = np.meshgrid(x,y)
Z = np.zeros_like(X)
```
We create an array for the Z values, and if rendered at this point, it would be a flat contour-less map.

Having archived a series of results files that we named by coordinate pairs, we can now retrieve them and assign each point of the grid a Z value.

```Python
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
```
We populate our interpolated model with new Z values, in this case the distance traveled.
```Python
f = interp2d(X, Y, Z, kind='linear')
X_fine,Y_fine = np.meshgrid(x_fine,y_fine)
Z_fine = f(x_fine, y_fine)
```
We can make a visual model of the initial data using the Matplotlib library in python.  The high and brighter colored spots reflect greater cost, the blue and low points reflect lower cost.

```Python
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.gca().invert_xaxis()
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma)
```
![Figure_map_a2](https://user-images.githubusercontent.com/77086418/107602021-f4001780-6bed-11eb-8bd7-107ecca93236.png)

Now we have enough information to render an interpolated map.  Here, we can visualize the difference between our initial data and our interpolated model.
```Python
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.gca().invert_xaxis()
surf = ax.plot_surface(X_fine, Y_fine, Z_fine, rstride=1, cstride=1, cmap=cm.plasma)
```
![figure-a1b1](https://user-images.githubusercontent.com/77086418/107456568-fe4ee280-6b15-11eb-87d5-b14cc33b6ceb.gif)

Visualizations are great, but not necessary for our purposes.  We can reuse our interp2d function to find any interpolated value within the grid.

```Python
test_coordinates = [30.312987, -97.828008]
distance = f(test_coordinates[0],test_coordinates[1])
````
