import pytest
from typing import List

from flask import g

from informatics_front.model import StatementProblem, Problem, Statement, Comment, db
from informatics_front.model.contest.contest_instance import ContestInstance
from informatics_front.model.problem import EjudgeProblem
from informatics_front.model.workshop.workshop import WorkShop, WorkshopStatus
from informatics_front.model.workshop.workshop_connection import WorkshopConnection

VALID_TIME = 100500
COURSE_VISIBLE = 1


@pytest.yield_fixture
def problem(app) -> dict:
    problem = Problem(
        content='foo',
        description='bar',
        memorylimit=100,
        name='baz',
        output_only=True,
        timelimit=3.14,
    )

    db.session.add(problem)
    db.session.commit()

    yield problem

    db.session.delete(problem)
    db.session.commit()


@pytest.yield_fixture
def workshop(app, statement):
    w = WorkShop(status=WorkshopStatus.ONGOING)
    db.session.add(w)
    db.session.flush()

    ci = ContestInstance(workshop_id=w.id, contest_id=statement.id)
    db.session.add(ci)
    db.session.flush()

    db.session.commit()

    yield {'workshop': w, 'contest_instance': ci}

    db.session.delete(ci)
    db.session.delete(w)
    db.session.commit()


@pytest.yield_fixture
def workshop_connection(authorized_user, workshop):
    w = workshop['workshop']

    wc = WorkshopConnection(workshop_id=w.id, user_id=g.user['id'])
    db.session.add(wc)
    db.session.commit()

    yield

    db.session.delete(wc)



@pytest.yield_fixture
def statement(app) -> dict:
    ejudge_problems = [
        EjudgeProblem.create(
            ejudge_prid=1,
            contest_id=1,
            ejudge_contest_id=1,
            problem_id=1,
        ),
        EjudgeProblem.create(
            ejudge_prid=2,
            contest_id=2,
            ejudge_contest_id=1,
            problem_id=2,
        ),
        EjudgeProblem.create(
            ejudge_prid=3,
            contest_id=3,
            ejudge_contest_id=2,
            problem_id=1,
        )
    ]
    db.session.add_all(ejudge_problems)
    db.session.flush(ejudge_problems)
    problems = [
        Problem(name='Problem1', pr_id=ejudge_problems[0].id),
        Problem(name='Problem2', pr_id=ejudge_problems[1].id),
        Problem(name='Problem3', pr_id=ejudge_problems[2].id),
    ]
    db.session.add_all(problems)
    db.session.flush(problems)
    statement = Statement(name='foo', summary='bar')
    db.session.add(statement)
    db.session.flush()

    statement_problems = [
        StatementProblem(problem_id=problems[0].id,
                         statement_id=statement.id,
                         rank=1),
        StatementProblem(problem_id=problems[1].id,
                         statement_id=statement.id,
                         rank=2),
        StatementProblem(problem_id=problems[2].id,
                         statement_id=statement.id,
                         rank=3),
    ]
    db.session.add_all(statement_problems)
    db.session.commit()

    yield statement

    for sp in statement_problems:
        db.session.delete(sp)
    db.session.commit()

    db.session.delete(statement)
    db.session.commit()



@pytest.yield_fixture
def problem(app) -> dict:
    problem = Problem(
        content='foo',
        description='bar',
        memorylimit=100,
        name='baz',
        output_only=True,
        timelimit=3.14,
        hidden=False,
    )

    db.session.add(problem)
    db.session.commit()

    yield problem

    db.session.delete(problem)
    db.session.commit()


@pytest.yield_fixture
def comments(app, users, authorized_user) -> List[dict]:
    author = users[-1]  # should not be the same as current authorized user

    comments_ = [
        Comment(
            comment=f'Comment for py_run_id #{py_run_id}',
            py_run_id=py_run_id,
            user_id=authorized_user.user['id'],
            author_user_id=author['id']
        ) for py_run_id in range(1, 4)
    ]

    db.session.add_all(comments_)
    db.session.commit()

    yield comments_

    db.session.query(Comment).delete()
    db.session.commit()


@pytest.yield_fixture
def comment(comments) -> dict:
    yield comments[0]
