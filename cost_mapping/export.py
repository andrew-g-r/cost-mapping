"""Portable cost-surface exports."""
import csv
import io

def csv_surface(surface):
    output=io.StringIO()
    writer=csv.writer(output)
    writer.writerow(['latitude','longitude','value','unit'])
    for i,lat in enumerate(surface.grid.latitudes):
        for j,lon in enumerate(surface.grid.longitudes):
            writer.writerow([lat,lon,surface.values[i][j],surface.unit])
    return output.getvalue()

def geojson_surface(surface):
    features=[]
    for i,lat in enumerate(surface.grid.latitudes):
        for j,lon in enumerate(surface.grid.longitudes):
            features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[lon,lat]},
                'properties':{'value':surface.values[i][j],'unit':surface.unit,'row':i,'column':j}})
    return {'type':'FeatureCollection','features':features,'source':surface.source}
