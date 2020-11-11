import os
import geocoder

g = geocoder.bing( 'Mountain View, CA', key=os.environ[ 'BING_API_KEY' ] )

print( g.json[ 'raw' ][ '__type' ] )


# --- END --- #

