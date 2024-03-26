from flask_sqlalchemy import SQLAlchemy
import csv


db = SQLAlchemy()


def load_initial_data(model, path_to_file: str) -> None:
    with open(path_to_file, "r") as f:
        csv_reader = csv.DictReader(f)
        fields = csv_reader.fieldnames
        for row in csv_reader:
            db_record = model(**{field: row[field] for field in fields})

            db.session.add(db_record)

        db.session.commit()

    db.session.close()



