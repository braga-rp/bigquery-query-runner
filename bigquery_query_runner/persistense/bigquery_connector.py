import logging
import os

from google.cloud import bigquery
from google.cloud.bigquery import QueryJob

from bigquery_query_runner.persistense.query_result import QueryResult

logging.basicConfig(format='[%(asctime)s]:[%(levelname)s]:[%(message)s]', level=logging.INFO)
NUM_LINES = 20


class BigQueryConnector:

    def __init__(self, full_table_name: str, output_file: str, output_format: str,
                 with_header: bool, single_output: bool):
        self.full_table_name = full_table_name
        self.output_file = output_file[:-1] if output_file and output_file.endswith("/") else output_file
        self._output_format = output_format.lower()
        self._with_header = with_header
        self._single_output = single_output

        default_project = os.environ.get("GCP_PROJECT")
        self.client = bigquery.Client(project=default_project) if default_project else bigquery.Client()

    def submit_query(self, query: str) -> QueryResult:
        # Executa consulta e aguarda resultado
        destination_table, sample = self._run_query_job(query)

        # Salva resultado num arquivo
        if self.output_file:
            destination_uri = self._export_table(destination_table)
        else:
            destination_uri = None

        return QueryResult(destination_uri, sample)

    def _run_query_job(self, query):
        if self.output_file:
            job_config = bigquery.QueryJobConfig()
            job_config.destination = self.full_table_name
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

            query_job: QueryJob = self.client.query(query, job_config=job_config)

            sample = _get_sample(query_job.result())

            return self.full_table_name, sample
        else:
            self.client.query(query).result()
            return self.full_table_name, []

    def _export_table(self, destination_table):
        multiple_suffix = "" if self._single_output else "/*"
        destination_uri = f"{self.output_file}{multiple_suffix}"

        job_config = self._create_job_config()

        extract_job = self.client.extract_table(destination_table, destination_uri, job_config=job_config)
        extract_job.result()
        return destination_uri

    def _create_job_config(self) -> bigquery.job.ExtractJobConfig:
        config = bigquery.job.ExtractJobConfig()

        if self._output_format == 'csv':
            config.print_header = self._with_header
            config.destination_format = 'CSV'
        if self._output_format == 'json':
            config.destination_format = "NEWLINE_DELIMITED_JSON"

        if self._output_format == "avro":
            config.destination_format = "AVRO"

        return config


def _get_sample(results):
    samples = []
    for index, result in enumerate(results):
        if index == 0:
            header = ','.join(result.keys())
            samples.append(header)

        if index == NUM_LINES:
            break

        sample = ','.join([str(_) for _ in result.values()])
        samples.append(sample)
    return samples
