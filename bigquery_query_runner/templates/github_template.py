from github import Github

from bigquery_query_runner.templates.parser import parse_query, split_parameters


class GithubTemplate:

    def __init__(self, token: str, organization: str, repository: str, reference: str):
        github = Github(login_or_token=token)
        org = github.get_organization(organization)

        self._repository = org.get_repo(repository)
        self._reference = reference

    def parse(self, template_path, params):
        params_dict = split_parameters(params) if params else {}

        query_template = self._get_query(template_path, self._reference)

        return parse_query(query_template, params_dict)

    def _get_query(self, template_path: str, reference: str):
        contents = self._repository.get_contents(template_path, ref=reference)
        return contents.decoded_content.decode('UTF-8')
