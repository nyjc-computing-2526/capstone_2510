"""
Run the app.
"""

from app_obj import app

# These imports mutate app
import routes.activities
import routes.landing

app.run()