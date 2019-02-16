from informatics_front.model.base import db
from informatics_front.model.course_module import CourseModuleInstance
from informatics_front.utils.functions import attrs_to_dict


class Resource(CourseModuleInstance, db.Model):
    """
    Модуль курса, описывающий ссылку
    """
    __table_args__ = {'schema': 'moodle'}
    __tablename__ = 'mdl_resource'
    __mapper_args__ = {
        'polymorphic_identity': 'resource',
        'concrete': True,
    }

    MODULE = 13

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column('course', db.Integer)
    name = db.Column(db.Unicode(255))
    type_ = db.Column('type', db.Unicode(30))
    reference = db.Column(db.Unicode(255))
    summary = db.Column(db.UnicodeText())

    def serialize(self):
        serialized = attrs_to_dict(
            self,
            'id',
            'course_id',
            'name',
            'type',
            'reference',
            'summary',
        )
        serialized['type'] = self.type_
        return serialized
