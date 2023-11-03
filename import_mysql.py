import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import create_database, database_exists, drop_database
from decouple import Config, RepositoryEnv
from Components.Models import Base, Gender, CustomerType, TypeOfTravel, Class, Satisfaction, Age, SatisfactionCustomer
import pandas as pd


########## Chemin du CSV brut

path_csv_brut = 'Data/Airline_Dataset.csv'

##########

# Fonctions de création des tables

def get_database_url():

    env_path = os.path.join(os.path.dirname(__file__), 'config/.env')
    config = Config(RepositoryEnv(env_path))

    host = config('MYSQL_HOST')
    port = config('MYSQL_PORT')
    database = config('MYSQL_DB')
    user = config('MYSQL_USER')
    password = config('MYSQL_PASSWORD')

    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"


def create_db(db_url):

    engine = create_engine(db_url)

    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database created: {engine.url}")
    else:
        print(f"Database already exists: {engine.url}")


def create_tables(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)


# Fonctions d'import dans MySQL

def insert_reference_data(session, model, column_name_df, column_name_db, format):
    if format == 'int':
        df[column_name_df] = df[column_name_df].astype('Int64').astype(object)
        df[column_name_df] = df[column_name_df].sort_values(
            ascending=True).values
    unique_values = df[column_name_df].unique()
    print(unique_values)
    for value in unique_values:
        if not session.query(model).filter_by(**{column_name_db: value}).first():
            session.add(model(**{column_name_db: value}))
    session.commit()


def insert_customer_satisfaction_data(session):
    for _, row in df.iterrows():

        gender_id = session.query(Gender.id).filter_by(
            gender_type=row['Gender']).scalar()
        customer_type_id = session.query(CustomerType.id).filter_by(
            type=row['Customer Type']).scalar()
        type_of_travel_id = session.query(TypeOfTravel.id).filter_by(
            travel_type=row['Type of Travel']).scalar()
        class_id = session.query(Class.id).filter_by(
            class_type=row['Class']).scalar()
        satisfaction_id = session.query(Satisfaction.id).filter_by(
            satisfaction_level=row['Satisfaction']).scalar()
        age_id = session.query(Age.id).filter_by(age=row['Age']).scalar()

        customer = SatisfactionCustomer(
            gender_id=gender_id,
            customer_type_id=customer_type_id,
            type_of_travel_id=type_of_travel_id,
            class_id=class_id,
            satisfaction_id=satisfaction_id,
            age_id=age_id,
            flight_distance=row['Flight Distance'],
            inflight_wifi_service=row['Inflight wifi service'],
            departure_arrival_time_convenient=row['Departure/Arrival time convenient'],
            ease_of_online_booking=row['Ease of Online booking'],
            gate_location=row['Gate location'],
            food_and_drink=row['Food and drink'],
            online_boarding=row['Online boarding'],
            seat_comfort=row['Seat comfort'],
            inflight_entertainment=row['Inflight entertainment'],
            on_board_service=row['On-board service'],
            leg_room_service=row['Leg room service'],
            baggage_handling=row['Baggage handling'],
            checkin_service=row['Checkin service'],
            inflight_service=row['Inflight service'],
            cleanliness=row['Cleanliness'],
            departure_delay_in_minutes=row['Departure Delay in Minutes'],
            arrival_delay_in_minutes=row['Arrival Delay in Minutes']
        )
        session.add(customer)
    session.commit()





# Création de l'adresse MySQL

DATABASE_URL = get_database_url()

# Création de l'engine MySQL

engine = create_engine(DATABASE_URL)

# Lancement de l'import dans MySQL

if database_exists(engine.url):
    drop_database(engine.url)
    print('Little bobby tables, he dropped it')


if not database_exists(engine.url):

    create_db(DATABASE_URL)
    create_tables(DATABASE_URL)

    # print_tables(DATABASE_URL)

    Session = sessionmaker(bind=engine)

    df = pd.read_csv(path_csv_brut)
    df['Arrival Delay in Minutes'].fillna(0, inplace=True)

    with Session() as session:
        insert_reference_data(session, Gender, 'Gender', 'gender_type', 'str')
        insert_reference_data(session, CustomerType,
                              'Customer Type', 'type', 'str')
        insert_reference_data(session, TypeOfTravel,
                              'Type of Travel', 'travel_type', 'str')
        insert_reference_data(session, Class, 'Class', 'class_type', 'str')
        insert_reference_data(session, Satisfaction,
                              'Satisfaction', 'satisfaction_level', 'str')
        insert_reference_data(session, Age, 'Age', 'age', 'int')
        '''
        resultat = session.query(Age).all()
        for i in resultat:
            print(f'id={i.id} - content={i.age}')
        '''
        insert_customer_satisfaction_data(session)

else:
    print(f"Database already exists: {engine.url}")


Session = sessionmaker(bind=engine)
session = Session()

# Décommenter pour générer les CSV de votre choix

# generate_csv(session, SatisfactionCustomer, 'Data/satisfaction_customers.csv')
# generate_csv(session, Gender, 'Data/Gender.csv')
# generate_csv(session, CustomerType, 'Data/CustomerType.csv')
# generate_csv(session, TypeOfTravel, 'Data/TypeOfTravel.csv')
# generate_csv(session, Class, 'Data/Class.csv')
# generate_csv(session, Satisfaction, 'Data/Satisfaction.csv')
# generate_csv(session, Age, 'Data/Age.csv')

# Requête SQL pour récupérer les données pour le ML
query = """
SELECT 
    sc.id, 
    g.gender_type, 
    ct.type AS customer_type, 
    tt.travel_type, 
    cl.class_type, 
    s.satisfaction_level, 
    a.age,
    sc.flight_distance,
    sc.inflight_wifi_service,
    sc.departure_arrival_time_convenient,
    sc.ease_of_online_booking,
    sc.gate_location,
    sc.food_and_drink,
    sc.online_boarding,
    sc.seat_comfort,
    sc.inflight_entertainment,
    sc.on_board_service,
    sc.leg_room_service,
    sc.baggage_handling,
    sc.checkin_service,
    sc.inflight_service,
    sc.cleanliness,
    sc.departure_delay_in_minutes,
    sc.arrival_delay_in_minutes
FROM 
    satisfaction_customers sc
JOIN 
    gender g ON sc.gender_id = g.id
JOIN 
    customer_type ct ON sc.customer_type_id = ct.id
JOIN 
    type_of_travel tt ON sc.type_of_travel_id = tt.id
JOIN 
    class cl ON sc.class_id = cl.id
JOIN 
    satisfaction s ON sc.satisfaction_id = s.id
JOIN 
    age a ON sc.age_id = a.id;
"""

col = ['id', 'Gender', 'Customer Type', 'Type of Travel', 'Class', 'Satisfaction',
       'Age', 'Flight Distance', 'Inflight wifi service',
       'Departure/Arrival time convenient', 'Ease of Online booking',
       'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
       'Inflight entertainment', 'On-board service', 'Leg room service',
       'Baggage handling', 'Checkin service', 'Inflight service',
       'Cleanliness', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
       ]

df = pd.read_sql_query(query, engine)

df.columns=col

# Exportez les résultats dans un fichier CSV

csv_file_path = 'Data/satisfaction_customers_export.csv'
df.to_csv(csv_file_path, index=False)

print(f'Les données ont été exportées avec succès dans le fichier {csv_file_path}')
