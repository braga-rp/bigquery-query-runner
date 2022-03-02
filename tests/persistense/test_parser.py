from unittest import TestCase

from bigquery_query_runner.persistense.parser import parse_query


class TestGithub(TestCase):

    def test_parse_simple_template(self):
        template = "select * from tabela where name = {{nome}} and id = {{id}}"
        expected = "select * from tabela where name = 'Usuário de Teste' and id = 12"

        params = dict(nome='Usuário de Teste', id=12)
        parsed = parse_query(template, params)

        assert parsed == expected

    def test_parse_template_with_condition_true(self):
        template = "select * from tabela where " \
                   "{%if nome %} " \
                   "name = {{nome}} " \
                   "{% endif %} " \
                   "and id = {{id}}"

        expected_with_nome = "select * from tabela where  " \
                             "name = 'Usuário de Teste'  " \
                             "and id = 12"
        params = dict(nome='Usuário de Teste', id=12)
        parsed = parse_query(template, params)
        assert parsed == expected_with_nome

    def test_parse_template_with_condition_false(self):
        template = "select * from tabela where " \
                   "{%if nome %} " \
                   "name = {{nome}} " \
                   "{% endif %} " \
                   "and id = {{id}}"

        expected_without_nome = "select * from tabela where  " \
                                "and id = 12"
        params = dict(id=12)
        parsed = parse_query(template, params)
        assert parsed == expected_without_nome

    def test_parse_with_repeated_parameters(self):
        template = "select name, data from table where name={{nome}} or identificador={{nome}}"
        expected = "select name, data from table where name='Usuário de Teste' or identificador='Usuário de Teste'"

        params = dict(nome='Usuário de Teste', id=12)
        parsed = parse_query(template, params)
        assert parsed == expected
