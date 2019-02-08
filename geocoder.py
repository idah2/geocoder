import geopy, sys, os, pandas
from geopy.geocoders import Nominatim, GoogleV3, Yandex
from tqdm import tqdm

inputfile=str(sys.argv[1])
outputfile=str(sys.argv[2])
outputjson=outputfile.replace('.csv', '.geojson')

def main():
  io = pandas.read_csv(inputfile, index_col=None, header=0, sep=",")

  def get_latitude(x):
    if x is not None:
      return x.latitude
    else:
      return 'not found'

  def get_longitude(x):
    if x is not None:
      return x.longitude
    else:
      return 'not found'

  geolocator = Nominatim(timeout=10)
  #geolocator = GoogleV3(timeout=20)
  #geolocator = Yandex(timeout=10)

  tqdm.pandas()

  helper = io['City'].map(str) + " " + io['State'].map(str) + " " + io['Country'].map(str)
  #helper = io['continent'].map(str)
  geolocate_column = helper.progress_apply(geolocator.geocode)
  io['latitude'] = geolocate_column.apply(get_latitude)
  io['longitude'] = geolocate_column.apply(get_longitude)
  io.to_csv(outputfile, index=False)
  #os.system('csv2geojson ' + outputfile + ' > ' + outputjson)

if __name__ == '__main__':
  main()