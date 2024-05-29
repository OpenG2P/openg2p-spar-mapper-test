import psycopg2
from psycopg2.extras import execute_values, Json
import datetime

# Database connection parameters
db_params = {
    "dbname": "spardb",
    "user": "postgres",
    "password": "6hpHncKeC3",
    "host": "explore.openg2p.net",
    "port": "5433",
}


def create_record(
    id_value, fa_value, name, phone, additional_info, created_at, updated_at, id, active
):
    return (
        id_value,
        fa_value,
        name,
        phone,
        Json(additional_info),
        created_at,
        updated_at,
        id,
        active,
    )


def insert_records_bulk(records, batch_size=1000):
    connection = None
    try:
        # Connect to the database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # SQL insert query
        insert_query = """
        INSERT INTO id_fa_mappings (id_value, fa_value, name, phone, additional_info, created_at, updated_at, id, active)
        VALUES %s
        """

        # Insert records in batches
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            execute_values(cursor, insert_query, batch)
            connection.commit()
            print(f"{len(batch)} records inserted successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        raise (f"Error: {error}")
    finally:
        if connection is not None:
            connection.close()


def generate_records(starting_id, end_id):
    records = []
    for i in range(starting_id, end_id + 1):
        record = create_record(
            f"id-{i}",
            f"fa-{i}",
            f"random_name-{i}",
            str(i),
            [],
            datetime.datetime.now(),
            datetime.datetime.now(),
            i,
            True,
        )
        records.append(record)
    return records


# Number of records to insert
STARTING_ID = 1
END_ID = 10000000
BATCH_SIZE = 5000  # Adjust the batch size as needed

# Generate records
print(f"Generating {END_ID} records...")
records = generate_records(STARTING_ID, END_ID)
print(f"Total {END_ID} records generated successfully.")

# Insert records in bulk
print(f"Inserting {END_ID} records in the database...")
insert_records_bulk(records, BATCH_SIZE)
print(f"Total {END_ID} records inserted successfully.")
