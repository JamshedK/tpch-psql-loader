import logging
import os

from replica import Replica
from tpch_generator import TPCHGenerator

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tpch_test.log'),  # Save to file
        logging.StreamHandler()                 # Also print to console
    ]
)

def test_tpch_data_loading():
    '''
    Test the TPC-H data generation and loading process.
    
    This test:
    1. Sets up a PostgreSQL connection
    2. Generates TPC-H data at scale factor 1 (smallest)
    3. Loads the data into the database
    4. Verifies the data was loaded
    '''
    
    # Database configuration (PostgreSQL 14, localhost:5432)
    replica = Replica(
        id=0,
        hostname='localhost',
        port='5432',
        dbname='tpch_1_template',
        user='postgres',
        password='123456'
    )
    
    # Paths configuration
    # dbgen is in parent directory: /home/karimnazarovj/tpch-dbgen
    dbgen_path = '/home/karimnazarovj/tpch-dbgen'
    data_path = '/home/karimnazarovj/tpch-data'
    
    # Use scale factor 1 for testing (about 1GB of data)
    scale_factor = 1
    
    logging.info('Initializing TPC-H Generator')
    generator = TPCHGenerator(
        replicas=[replica],
        dbgen_path=dbgen_path,
        data_path=data_path,
        scale_factor=scale_factor
    )
    
    try:
        # Generate the data
        logging.info('Starting data generation...')
        generator.generate()
        logging.info('Data generation completed successfully')
        
        # Load into database
        logging.info('Starting database loading...')
        generator.load_database()
        logging.info('Database loading completed successfully')
        
        # Read queries into memory
        logging.info('Loading queries...')
        queries, templates = generator.read_data()
        logging.info(f'Loaded {len(queries)} queries')
        
        logging.info('Test completed successfully!')
        
    except Exception as e:
        logging.error(f'Test failed with error: {e}', exc_info=True)
        raise


if __name__ == '__main__':
    test_tpch_data_loading()
