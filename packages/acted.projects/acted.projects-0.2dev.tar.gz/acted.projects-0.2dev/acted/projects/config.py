"""Common configuration constants
"""
from Products.Archetypes.public import DisplayList

###########################################################################
## ACTED only change what is between the ######## lines !!!!!
## ivan.price@acted.org   14/6/2010
## 
## After changing this file you need to restart plone !

theYears = range(1995,2016)

theDonors = (
'US AID',
'ECHO',
'GTZ'
)


theSectors = (
'NFI',
'Shelter',
'WASH'
)


theCountries = (
'Afghanistan',
'Central African Republic',
'Chad',
'Democratic Republic of Congo',
'France',
'Haiti',
'India',
'Indonesia',
'Iraq',
'Jordan',
'Kenya',
'Kyrgyzstan',
'Lebanon',
'Myanmar',
'Nicaragua',
'Occupied Palestinian Territories',
'Pakistan',
'Republic of Congo',
'Somalia',
'Sri Lanka',
'Sudan',
'Tajikistan',
'Uganda'
)



############################################################################

ACTED_DONORS = DisplayList()
for donor in theDonors:
   ACTED_DONORS.add(donor,donor)

ACTED_COUNTRIES = DisplayList()
for country in theCountries:
   ACTED_COUNTRIES.add(country,country)

ACTED_SECTORS = DisplayList()
for sector in theSectors:
   ACTED_SECTORS.add(sector,sector)

ACTED_YEARS = DisplayList()
for year in theYears:
   ACTED_YEARS.add(year,year)


PROJECTNAME = 'acted.projects'
ADD_PERMISSIONS = {
    'ACTEDProject': 'acted.projects: Add ACTED Project',
}
