import csv

from extensions import db
from controllers.database.zip import Zip

def load():

    existing_data = Zip.query.count()
    print('ZIP', existing_data)
    if existing_data:
        db.session.query(Zip).delete()

    with open('data/geocorr14.csv', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, ['zip', 'fip_state', 'cd114', 'state',
                                          'zip_name', 'pop', 'factor'])
        # 2 line header
        next(reader)
        next(reader)
        for row in reader:
            db.session.add(Zip(row['zip'], row['state'], row['cd114'],
                               row['factor']))
            db.session.commit()
      
