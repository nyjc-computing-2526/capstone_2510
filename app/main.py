"""
Run the app.
"""

from app_obj import app

# These imports mutate the app object
import routes.activities
import routes.authentication
import routes.landing

app.run()