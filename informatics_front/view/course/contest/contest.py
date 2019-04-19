from typing import Optional, List

from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Load, joinedload
from werkzeug.exceptions import NotFound, Forbidden

from informatics_front import current_user
from informatics_front.model import Problem, StatementProblem
from informatics_front.model.base import db
from informatics_front.model.contest.contest import Contest
from informatics_front.model.workshop.contest_connection import ContestConnection
from informatics_front.model.workshop.workshop_connection import WorkshopConnection, WorkshopConnectionStatus
from informatics_front.utils.auth import login_required
from informatics_front.utils.response import jsonify
from informatics_front.view.course.contest.serializers.contest import ContestConnectionSchema


class ContestApi(MethodView):
    @login_required
    def get(self, contest_id):
        contest: Contest = db.session.query(Contest) \
                            .options(joinedload(Contest.statement)) \
                            .options(joinedload(Contest.workshop)) \
                            .get(contest_id)

        if contest is None:
            raise NotFound(f'Cannot find contest module id #{contest_id}')

        user_id = current_user.id
        self._check_workshop_permissions(user_id,
                                         contest.workshop)

        cc = self._get_contest_connection(user_id, contest.id) or \
            self._create_contest_connection(user_id, contest.id)

        if not contest.is_available(cc):
            raise Forbidden('Contest is not started or already finished')

        contest.statement.problems = self._load_problems(contest.statement_id)
        cc.contest = contest

        cc_schema = ContestConnectionSchema()

        response = cc_schema.dump(cc)

        return jsonify(response.data)

    @staticmethod
    def _load_problems(statement_id) -> List[Problem]:
        """ Load Problems from Statement """
        problems_statement_problems = db.session.query(Problem, StatementProblem) \
            .join(StatementProblem, StatementProblem.problem_id == Problem.id) \
            .filter(StatementProblem.statement_id == statement_id) \
            .filter(StatementProblem.hidden == 0) \
            .options(Load(Problem).load_only('id', 'name')) \
            .options(Load(StatementProblem).load_only('rank'))

        problems = []
        # Yes it is ugly but I think its better than rewrite query
        for problem, sp in problems_statement_problems.all():
            problem.rank = sp.rank
            problems.append(problem)

        return problems

    @classmethod
    def _check_workshop_permissions(cls, user_id, workshop) -> Optional[WorkshopConnection]:
        workshop_connection = db.session.query(WorkshopConnection) \
                                        .filter_by(user_id=user_id,
                                                   workshop_id=workshop.id) \
                                        .one_or_none()
        if workshop_connection is not None and workshop_connection.is_accepted():
            return workshop_connection
        raise NotFound('Contest is not found')

    @classmethod
    def _get_contest_connection(cls, user_id: int, contest_id: int) \
            -> Optional[ContestConnection]:
        """ Returns user connection on contest instance"""
        cc = db.session.query(ContestConnection) \
            .filter_by(user_id=user_id, contest_id=contest_id) \
            .one_or_none()
        return cc

    @classmethod
    def _create_contest_connection(cls, user_id, contest_id: int) -> ContestConnection:
        """ Beware: we use COMMIT and ROLLBACK in this function! """
        cc = ContestConnection(user_id=user_id, contest_id=contest_id)
        db.session.begin_nested()
        try:
            db.session.add(cc)
            db.session.commit()
            db.session.refresh(cc)
        except IntegrityError:
            db.session.rollback()
            cc = cls._get_contest_connection(user_id, contest_id)
        return cc
