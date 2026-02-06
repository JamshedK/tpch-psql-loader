import os
import subprocess
import glob
import shutil
import random


class TPCHQueryGenerator:
    def __init__(self, dbgen_path: str, scale_factor: int, queries_per_template: int = 2):
        """
        Simple TPC-H query generator that only generates queries.
        
        :param dbgen_path: path to the dbgen directory containing qgen executable
        :param scale_factor: TPC-H scale factor
        :param queries_per_template: number of queries to generate per template (default: 2)
        """
        self.dbgen_path = dbgen_path
        self.scale_factor = str(scale_factor)
        self.queries_per_template = queries_per_template
        self.root_dir = os.path.dirname(os.path.realpath(__file__))
    
    def generate_queries(self, output_folder: str):
        """
        Generate queries and save them to workloads/{output_folder}/
        
        :param output_folder: name of the folder under workloads/ (e.g., '440_queries_out')
        """
        output_path = f'{self.root_dir}/workloads/{output_folder}'
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        print(f'Created output directory: {output_path}')
        
        # Copy query templates if needed
        self._setup_query_templates()
        
        # Generate queries in batches - each batch uses the same seed for all 22 templates
        query_count = 0
        for batch_num in range(1, self.queries_per_template + 1):
            # Generate a seed for this batch of 22 queries
            seed = random.randint(1, 1000000)
            print(f'\nBatch {batch_num} (seed: {seed}):')
            
            for template_num in range(1, 23):
                output_file = f'{output_path}/q{template_num}_{batch_num}.sql'
                self._generate_single_query(template_num, seed, output_file)
                query_count += 1
                print(f'  Generated query {query_count}/{22 * self.queries_per_template}: {os.path.basename(output_file)}')
        
        print(f'\nSuccessfully generated {query_count} queries in {output_path}')
    
    def _setup_query_templates(self):
        """Copy corrected query templates to dbgen/queries directory"""
        dbgen_queries_dir = f'{self.dbgen_path}/queries'
        os.makedirs(dbgen_queries_dir, exist_ok=True)
        
        corrected_templates = glob.glob(f'{self.root_dir}/tpch-templates/*.sql')
        
        if corrected_templates:
            for template in corrected_templates:
                shutil.copy(template, dbgen_queries_dir)
    
    def _generate_single_query(self, template_num: int, seed: int, output_file: str):
        """Generate a single query from a template using the provided seed"""
        with open(output_file, 'w') as outfile:
            subprocess.run(
                [f'{self.dbgen_path}/qgen', '-r', str(seed), '-s', self.scale_factor, str(template_num)],
                cwd=self.dbgen_path,
                env=dict(os.environ, DSS_QUERY=f'{self.dbgen_path}/queries'),
                stdout=outfile,
                stderr=subprocess.DEVNULL
            )


def main():
    """Main function to generate TPC-H queries"""
    
    # Configuration
    dbgen_path = '/home/karimnazarovj/tpch-dbgen'  # Update this path as needed
    scale_factor = 1
    queries_per_template = 4
    output_folder = f'{22 * queries_per_template}_queries_out'
    
    print(f'TPC-H Query Generator')
    print(f'=====================')
    print(f'Scale Factor: {scale_factor}')
    print(f'Queries per Template: {queries_per_template}')
    print(f'Total Queries: {22 * queries_per_template}')
    print(f'Output Folder: workloads/{output_folder}')
    print()
    
    # Generate queries
    generator = TPCHQueryGenerator(
        dbgen_path=dbgen_path,
        scale_factor=scale_factor,
        queries_per_template=queries_per_template
    )
    
    generator.generate_queries(output_folder)


if __name__ == '__main__':
    main()
