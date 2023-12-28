# NOTICE. ONLY USING COPY_CSV_FILES function. Originally used this file to create tables,
  # but wanted to learn Django Models to create data schemas.

# This is a schema.sql file
import psycopg2
from psycopg2 import sql

# Import function to execute SQL queries
from index import conn

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

create_tables_sql = '''
CREATE TABLE IF NOT EXISTS snowboards (
  snowboard_id INTEGER PRIMARY KEY NOT NULL,
  snowboard_name VARCHAR(255) NOT NULL,
  header_image VARCHAR(255) NOT NULL,
  header_description TEXT NOT NULL,
  snowboard_price NUMERIC NOT NULL,
  shape VARCHAR(255) NOT NULL,
  sidecut VARCHAR(255) NOT NULL,
  flex VARCHAR(255) NOT NULL,
  rider_type VARCHAR(255) NOT NULL,
  tech_story TEXT NOT NULL,
  camber_type VARCHAR(255) NOT NULL,
  camber_description TEXT NOT NULL,
  camber_image VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS snowboard_images (
  snowboard_image_id INTEGER PRIMARY KEY NOT NULL,
  snowboard_image VARCHAR(255) NOT NULL,
  snowboard_id INTEGER NOT NULL,
  FOREIGN KEY (snowboard_id) REFERENCES snowboards(snowboard_id)
);

CREATE TABLE IF NOT EXISTS snowboard_reviews (
  review_id SERIAL PRIMARY KEY NOT NULL,
  snowboard_review_title VARCHAR(255) NOT NULL,
  snowboard_review_author VARCHAR(255) NOT NULL,
  snowboard_review_date DATE NOT NULL,
  snowboard_review_body TEXT NOT NULL,
  snowboard_review_rating INTEGER NOT NULL,
  snowboard_id INTEGER NOT NULL,
  FOREIGN KEY (snowboard_id) REFERENCES snowboards(snowboard_id)
);

CREATE TABLE IF NOT EXISTS snowboard_skus (
  snowboard_sku_id INTEGER PRIMARY KEY NOT NULL,
  snowboard_size VARCHAR(255) NOT NULL,
  snowboard_sku NUMERIC NOT NULL,
  snowboard_id INTEGER NOT NULL,
  FOREIGN KEY (snowboard_id) REFERENCES snowboards(snowboard_id)
);

CREATE TABLE IF NOT EXISTS tshirts (
  tshirt_id INTEGER PRIMARY KEY NOT NULL,
  tshirt_name VARCHAR(255) NOT NULL,
  tshirt_price NUMERIC NOT NULL,
  tshirt_image VARCHAR(255) NOT NULL,
  tshirt_description TEXT
);

CREATE TABLE IF NOT EXISTS tshirt_skus (
  tshirt_sku_id INTEGER PRIMARY KEY NOT NULL,
  tshirt_size VARCHAR(255) NOT NULL,
  tshirt_sku NUMERIC NOT NULL,
  tshirt_id INTEGER NOT NULL,
  FOREIGN KEY (tshirt_id) REFERENCES tshirts(tshirt_id)
);

CREATE TABLE IF NOT EXISTS hoodies (
  hoodie_id INTEGER PRIMARY KEY NOT NULL,
  hoodie_name VARCHAR(255) NOT NULL,
  hoodie_price NUMERIC NOT NULL,
  hoodie_image VARCHAR(255) NOT NULL,
  hoodie_description TEXT
);

CREATE TABLE IF NOT EXISTS hoodie_skus (
  hoodie_sku_id INTEGER PRIMARY KEY NOT NULL,
  hoodie_size VARCHAR(255) NOT NULL,
  hoodie_sku NUMERIC NOT NULL,
  hoodie_id INTEGER NOT NULL,
  FOREIGN KEY (hoodie_id) REFERENCES hoodies(hoodie_id)
);

CREATE TABLE IF NOT EXISTS headgear (
  headgear_id INTEGER PRIMARY KEY NOT NULL,
  headgear_name VARCHAR(255) NOT NULL,
  headgear_image VARCHAR(255) NOT NULL,
  headgear_price NUMERIC NOT NULL,
  headgear_description TEXT,
  headgear_sku NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS boardbag (
  boardbag_id INTEGER PRIMARY KEY NOT NULL,
  boardbag_name VARCHAR(255) NOT NULL,
  boardbag_price NUMERIC NOT NULL,
  boardbag_size VARCHAR(255),
  boardbag_description TEXT,
  boardbag_sku NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS boardbag_images (
  boardbag_image_id INTEGER PRIMARY KEY NOT NULL,
  boardbag_image VARCHAR(255) NOT NULL,
  boardbag_id INTEGER NOT NULL,
  FOREIGN KEY (boardbag_id) REFERENCES boardbag(boardbag_id)
);

CREATE INDEX snowboard_images_snowboard_id_index ON snowboard_images(snowboard_id);
CREATE INDEX snowboard_reviews_snowboard_id_index ON snowboard_reviews(snowboard_id);
CREATE INDEX snowboard_skus_snowboard_id_index ON snowboard_skus(snowboard_id);
CREATE INDEX tshirt_skus_tshirt_id_index ON tshirt_skus(tshirt_id);
CREATE INDEX hoodie_skus_hoodie_id_index ON hoodie_skus(hoodie_id);
CREATE INDEX boardbag_images_boardbag_id_index ON boardbag_images(boardbag_id);
'''

FILE_PATH = os.getenv('FILE_PATH')

copy_csv_files = f'''
COPY snowboards FROM '{FILE_PATH}snowboards/snowtum_shredders_snowboards.csv' CSV HEADER;
COPY snowboard_images FROM '{FILE_PATH}snowboards/snowtum_shredders_snowboard_images.csv' CSV HEADER;
UPDATE snowboard_images
SET snowboard_image = CONCAT('https://', snowboard_image);
COPY snowboard_reviews FROM '{FILE_PATH}snowboards/snowtum_shredders_snowboard_reviews.csv' CSV HEADER;
COPY snowboard_skus FROM '{FILE_PATH}snowboards/snowtum_shredders_snowboard_skus.csv' CSV HEADER;
COPY tshirts FROM '{FILE_PATH}tshirts/snowtum_shredders_tshirts.csv' CSV HEADER;
UPDATE tshirts
SET tshirt_image = CONCAT('https://', tshirt_image);
COPY tshirt_skus FROM '{FILE_PATH}tshirts/snowtum_shredders_tshirt_skus.csv' CSV HEADER;
COPY hoodies FROM '{FILE_PATH}hoodies/snowtum_shredders_hoodies.csv' CSV HEADER;
UPDATE hoodies
SET hoodie_image = CONCAT('https://', hoodie_image);
COPY hoodie_skus FROM '{FILE_PATH}hoodies/snowtum_shredders_hoodie_skus.csv' CSV HEADER;
COPY headgear FROM '{FILE_PATH}snowtum_shredders_headgear.csv' CSV HEADER;
UPDATE headgear
SET headgear_image = CONCAT('https://', headgear_image);
COPY boardbag FROM '{FILE_PATH}boardbag/snowtum_shredders_boardbag.csv' CSV HEADER;
COPY boardbag_images FROM '{FILE_PATH}boardbag/snowtum_shredders_boardbag_image.csv' CSV HEADER;
UPDATE boardbag_images
SET boardbag_image = CONCAT('https://', boardbag_image);
SELECT setval('snowboard_reviews_review_id_seq', (SELECT MAX(review_id) FROM snowboard_reviews));
'''

# Function to execute PSQL Statements with no returned results
def execute_sql(sql_query):
    with conn.cursor() as cursor:
        cursor.execute(sql_query)
    conn.commit()

try:
  # # Execute CREATE TABLE statements
  # execute_sql(create_tables_sql)

 # Execute COPY CSV FILES into database
  execute_sql(copy_csv_files)
except psycopg2.Error as e:
  print('Error connecting/creating tables to PSQL', e)

finally:
  if conn:
    conn.close()
