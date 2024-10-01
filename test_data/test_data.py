from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_config
from src.infra.postgres.tables import Breed, Kitten

cfg = get_config()
# Create a session to interact with the database
engine = create_engine(cfg.database.migrate_dsn)
Session = sessionmaker(bind=engine)
session = Session()

breeds = [
    Breed(name='Siamese'),
    Breed(name='Persian'),
    Breed(name='Maine Coon'),
    Breed(name='British Shorthair'),
    Breed(name='Russian Blue')
]

session.add_all(breeds)
session.commit()

kittens = [
    Kitten(breed_id=breeds[0].id, color=' Seal Point', age=3, description='Playful and curious'),
    Kitten(breed_id=breeds[1].id, color='Lilac Point', age=2, description='Affectionate and lazy'),
    Kitten(breed_id=breeds[2].id, color='White', age=1, description='Energetic and playful'),
    Kitten(breed_id=breeds[3].id, color='Brown Tabby', age=4, description='Laid-back and gentle'),
    Kitten(breed_id=breeds[4].id, color='Grey', age=3, description='Curious and adventurous'),
    Kitten(breed_id=breeds[0].id, color='Blue', age=2, description='Shy and timid')
]

session.add_all(kittens)
session.commit()
