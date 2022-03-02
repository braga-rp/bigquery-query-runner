import random
import string

import click

from bigquery_query_runner.utils.kfp_utils import results_to_kfp
from bigquery_query_runner.persistense.bigquery_connector import BigQueryConnector
from bigquery_query_runner.templates.github_template import GithubTemplate
from bigquery_query_runner.utils.parameters_utils import get_env


@click.command()
@click.option('--github-token', type=str, default=get_env('GITHUB_TOKEN'),
              help="Github access token with repository permissions")
@click.option('--github-organization', type=str,
              help="Github organization where repository is")
@click.option('--github-repository', type=str, required=True, help="Github repository where template file is")
@click.option('--template-git-reference', type=str, default="main",
              help="Git reference (branch, tag, commit, etc) to refer the template file")
@click.option('--query-template-path', type=str, required=True,
              help="path to template file relative to repository root")
@click.option('--default-project', type=str, default=get_env("GCP_PROJECT"))
@click.option("--output-dataset", type=str, default="_temporary")
@click.option("--output-folder", type=str, default=None)
@click.option("--output-file", type=str, default=None)
@click.option("--output-format", type=click.Choice(["csv", "json", "avro"], case_sensitive=False), default="csv")
@click.option("--header/--no-header", default=True)
@click.option("--single-output/--multiple-output", default=True)
@click.option("--is-kubeflow/--is-not-kubeflow", default=False)
@click.argument('parameters', nargs=-1)
def main(github_token: str, github_organization: str, github_repository: str, template_git_reference: str,
         query_template_path, default_project: str, output_dataset: str, output_folder: str, output_file: str,
         output_format: str, header: bool, is_kubeflow: bool, parameters, single_output):

    if (output_file is not None) and (output_folder is not None):
        raise ValueError("Choose between --output-folder or --output-file")

    if (output_file is not None) and (not single_output):
        raise ValueError("You can't use --output-file parameter with --multiple-output flag")

    if output_folder is not None:
        rand = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        output_file = f"{output_folder}/{rand}.{output_format.lower()}"

    template_loader = GithubTemplate(github_token, github_organization,
                                     github_repository, template_git_reference)
    query = template_loader.parse(query_template_path, parameters)

    rand = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    full_table_name = f"{default_project}.{output_dataset}.query_{rand}"

    result = BigQueryConnector(full_table_name, output_file, output_format, header, single_output).submit_query(query)

    if output_file:
        print("Collected result:")
        for line in result.sample:
            print(line)

        print("Results file: ", result.file_path)

        results_to_kfp(result, is_kubeflow)


if __name__ == '__main__':
    main()
