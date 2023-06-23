import os

# This defines the base dir for all relative imports for our project, put the file in your root folder so the
# base_dir points to the root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'LcULz8NMxj~za0[#gp.h4])1frv[jwasLcULz8NMxj~za0[#gp'
# According to your data file, you can change the engine, like mysql, postgresql, mongodb etc make sure your data is
# directly placed in the same folder as this file, if it is not, please direct the 'NAME' field to its actual path.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'data', "db.sqlite3"),
    }
}

DISCORD = 'https://discord.com/api/webhooks/1104150221103042590/Fs3Uz2Otib2FhfT7u2QpOqrmE2U78cuREHHZ6HrAtbKweBYBj55J9x33ZAx5Bl9MPaO4'



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432
#     }
# }

#Since we only have one app which we use
INSTALLED_APPS = (
    'db',
)

# Write a random secret key here