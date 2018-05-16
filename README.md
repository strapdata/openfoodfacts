Python Meetup
=============

**Require python3**

Get the Open Food Fact CSV :
```
wget https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv -O resources/fr.openfoodfacts.org.products.csv
```

Install the dependencies:
```
pip install -r requirements.txt
```

Import the data:
```
python -m meetup.import
```

Start the web server:
```
python -m meetup.web
```