from marshmallow import fields, Schema

from informatics_front.model.problem import Problem


class ProblemSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    #content = fields.String(dump_only=True)
    content = fields.Method(serialize='fix_content')
    timelimit = fields.Float(dump_only=True)
    memorylimit = fields.Integer(dump_only=True)
    description = fields.String(dump_only=True)
    sample_tests_json = fields.Method(serialize='serialize_sample_tests')
    output_only = fields.Boolean(dump_only=True)

    def serialize_sample_tests(self, obj: Problem):
        obj.ejudge_problem.generate_samples_json()
        return obj.ejudge_problem.sample_tests_json

    def fix_content(self, obj: Problem):
        return obj.content.replace("\\(", "$").replace("\\)", "$")
