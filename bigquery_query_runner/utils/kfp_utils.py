import json

from bigquery_query_runner.persistense.query_result import QueryResult


def results_to_kfp(result: QueryResult, is_kubeflow: bool):
    base_path = "/" if is_kubeflow else "./"
    metadata = {
        'outputs': [{
            'type': 'table',
            'storage': 'inline',
            'format': 'csv',
            'source': "\n".join(result.sample)
        }]
    }

    metadata_path = base_path + 'mlpipeline-ui-metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

    outputs_path = base_path + "output.txt"
    print(f"Salvando {outputs_path}")
    with open(outputs_path, 'w') as f:
        f.write(result.file_path)
