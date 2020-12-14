import os
import geocoder

g = geocoder.bing( 'Newport News, VA', key=os.environ[ 'BING_API_KEY' ] )
print( g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )

g = geocoder.bing( 'Kenosha, WI', key=os.environ[ 'BING_API_KEY' ] )
print( g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )

# --- END --- #

