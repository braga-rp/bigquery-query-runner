# Runner of query templates on Google Cloud BigQuery
A tool for running a query template from a GitHub repository 
on Google Cloud BigQuery and saving the results file on a bucket in 
Google Cloud Storage.

This tool was build by six hands, the other four you can find here
- [Andre claudino](https://github.com/andreclaudino) 
- [Rômulo Tavares](https://github.com/tavaresrft)

## How to install
After cloning the repo one can ```cd``` to the projects root folder and install
using pip as

```bash
$ pip install bigquery-query-runner
```
or via Makefile with
```bash
$ make resources/install
```

## How to use
After installed ```bigquery-query-runner``` one can run as any other tool. From the terminal executing the entrypoint
```run-query```
command or run 

```bash
$ run-query --help 
```
for help.

The required parameters are 

|          parameters           | type | default                   |                                           help                                            |
|:-----------------------------:|:----:|:--------------------------|:-----------------------------------------------------------------------------------------:|
|         github-token          | str  | from env var GITHUB_TOKEN |                      Github access token with repository permissions                      |
|      github-organization      | str  | None                      |                          Github organization where repository is                          |
|       github-repository       | str  | None                      |                         Github repository where template file is                          |
|    template-git-reference     | str  | main                      |            Git reference (branch, tag, commit, etc) to refer the template file            |
|      query-template-path      | str  | None                      |                path to template file relative to repository root on GitHub                |
|        default-project        | str  | from env var GCP_PROJECT  |                        The gcp project wich one will run the query                        |
|        output-dataset         | str  | _temporary                |                   The dataset where the bigquery table will be created                    |               
|         output-folder         | str  | None                      |      The Google Cloud Storage folder where the file with query results will be saved      |
|          output-file          | str  | None                      |                  Path to the file where the query results will be saved                   |
|         output-format         | str  | csv                       |            Extension of the saved file. One can choose one of csv, json, avro             |
|       header/no-header        |      | True                      | If the file extension is csv choose this flag to generate a file with header or no header |
| single-output/multiple-output |      | True                      |              Choose if the output will be in a single file or multiple files              |              |
|  is-kubeflow/is-not-kubeflow  | |False|                          Generate or not a kubeflow output file                           |

The query parameters are passed as command line parameters
```bash
parameter_1=value_1 parameter_2=value_2 parameter_3=value_3 ... 
```
Suppose one have the following query template stored in ```my_company``` GitHub in the project called ```my_project``` 
and branch ```other_branch``` and one want to save the output file as ```multiples json``` files. Thus, one will have 
to execute
```sql
SELECT
    name,
    birth_date
FROM
    my_table
WHERE
    name={{name_placeholder}}
    AND
    birth_date > PARSE_TIMESTAMP('%%Y-%%m-%%d', {{birth_date_placeholder}})
```

```bash
run-query \
      --github-token=<toekn>\
      --github-organization=my_company\
      --github-repository=my_project \
      --template-git-reference=other_branch \
      --query-template-path=templates/query \
      --default-project=my_gcp_project \
      --output-file=gs://<project>/<bucket>/<folder>/* \
      --output-format=json \
      --multiple-output \
      --is-not-kubeflow \
      name_placeholder=my_name birth_date_placeholder=0001/02/03
```

Note that in the command written above one must choose between ```output-folder``` or ```output-file``` once the 
extension was json the ```header/no-header``` flag doesn't make sense.

## Run with docker

Assuming the example of the previous section. First pull the docker image 

```bash
docker pull docker.io/pedrorangelbraga/bigquery-query-runner:1.0.0
```

and run with
```bash
docker run -it \
      docker.io/pedrorangelbraga/bigquery-query-runner:1.0.0 \
      --github-token=<toekn>\
      --github-organization=my_company\
      --github-repository=my_project \
      --template-git-reference=other_branch \
      --query-template-path=templates/query \
      --default-project=my_gcp_project \
      --output-file=gs://<project>/<bucket>/<folder>/* \
      --output-format=json \
      --multiple-output \
      --is-not-kubeflow \
      name_placeholder=my_name birth_date_placeholder=0001/02/03
```