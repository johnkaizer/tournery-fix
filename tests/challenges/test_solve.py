#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from Tourney.exceptions.challenges import ChallengeSolveException
from Tourney.models import Solves
from Tourney.plugins.challenges import CHALLENGE_CLASSES
from tests.helpers import create_tourney, destroy_tourney, gen_challenge, gen_solve, gen_user


def test_solve_raises_challengesolveexception_on_duplicate():
    """
    BaseChallenge.solve() must convert a duplicate-solve IntegrityError into
    ChallengeSolveException, and must leave the original solve row intact.
    """
    app = create_tourney()
    with app.app_context():
        user = gen_user(app.db)
        challenge = gen_challenge(app.db)

        gen_solve(
            app.db,
            user_id=user.id,
            challenge_id=challenge.id,
            provided="flag{test}",
        )

        chal_class = CHALLENGE_CLASSES["standard"]

        with app.test_request_context(
            "/api/v1/challenges/attempt",
            method="POST",
            json={"submission": "flag{test}", "challenge_id": challenge.id},
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        ) as ctx:
            with pytest.raises(ChallengeSolveException):
                chal_class.solve(
                    user=user,
                    team=None,
                    challenge=challenge,
                    request=ctx.request,
                )

        solve_count = Solves.query.filter_by(
            account_id=user.account_id, challenge_id=challenge.id
        ).count()
        assert solve_count == 1

    destroy_tourney(app)