from marshmallow import Schema, fields, validate


class AIConfigSchema(Schema):
    provider = fields.Str(load_default=None)
    base_url = fields.Str(load_default=None)
    api_key = fields.Str(load_default=None)
    model = fields.Str(load_default=None)
    prompt = fields.Str(load_default=None)


class SubmissionCreateRequestSchema(Schema):
    url = fields.Str(required=True)
    platform = fields.Str(required=True, validate=validate.OneOf(["luogu", "codeforces"]))
    code = fields.Str(load_default=None)
    problem_name = fields.Str(load_default=None)
    ai_config = fields.Nested(AIConfigSchema, load_default=None)


class EnumField(fields.Field):
    """序列化 SQLAlchemy Enum / Python Enum 为字符串值"""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if hasattr(value, "value"):
            return value.value
        return str(value)


class SubmissionResponseSchema(Schema):
    id = fields.Int()
    platform = EnumField()
    submission_url = fields.Str()
    problem_id = fields.Str()
    problem_name = fields.Str()
    problem_url = fields.Str(allow_none=True)
    difficulty = fields.Str(allow_none=True)
    status = EnumField()
    failed_test_case = fields.Int(allow_none=True)
    created_at = fields.DateTime()


class MistakeResponseSchema(Schema):
    id = fields.Int()
    submission_id = fields.Int()
    error_category = fields.Str()
    error_severity = fields.Str()
    error_summary = fields.Str()
    error_detail = fields.Str()
    suggestion = fields.Str(allow_none=True)
    hints = fields.List(fields.Str(), allow_none=True)
    error_points = fields.List(fields.Str(), allow_none=True)
    reflection = fields.Str(allow_none=True)
    resolved = fields.Boolean()
    created_at = fields.DateTime()


class MistakeDetailResponseSchema(MistakeResponseSchema):
    submission = fields.Nested(SubmissionResponseSchema, allow_none=True)


class StatsResponseSchema(Schema):
    total_mistakes = fields.Int()
    by_category = fields.Dict(keys=fields.Str(), values=fields.Int())
    by_platform = fields.Dict(keys=fields.Str(), values=fields.Int())
    by_severity = fields.Dict(keys=fields.Str(), values=fields.Int())
    recent_trend = fields.List(fields.Dict())


class HintResponseSchema(Schema):
    hint = fields.Str()
    index = fields.Int()
    remaining = fields.Int()


class ResolveResponseSchema(Schema):
    message = fields.Str()
    mistake_id = fields.Int()
