# Duplicate solve records (and 500 errors) on repeated correct submissions

## The bug

Duplicate `Solves` rows appear for the same user or team on the same
challenge, and players sometimes get a 500 error when submitting. A solve is
meant to be unique per account per challenge, and the database enforces that
with a unique constraint, but the application can still attempt a second
insert; when it does, the constraint violation surfaces as an unhandled
error.

There are **two independent routes** to that second insert. Both need fixing.

## Route 1: player submission (`POST /api/v1/challenges/attempt`)

A correct answer records a `Solves` row through the challenge plugin's
`solve()` method. The endpoint checks "has this account already solved this
challenge?" before recording, but when the same correct answer arrives twice
in quick succession (a double click, a retried request, two open tabs), both
requests can pass that check before either has inserted:

| step | request A | request B |
|---|---|---|
| 1 | already solved? no | |
| 2 | | already solved? no |
| 3 | insert `Solves` row: ok | |
| 4 | | insert `Solves` row: constraint violation, player sees **500** |

Required behaviour: a duplicate correct submission must not error and must
not create a second solve. The endpoint treats it as an already-solved
success.

(The check at step 1 already handles the plain non-race case; what is missing
is the path where both requests pass the check.)

## Route 2: admin re-grade (`PATCH /api/v1/submissions/<id>`)

When an admin marks a submission as `correct`, a `Solves` row is created
unconditionally. If the player already has a solve for that challenge, the
insert hits the same constraint and the admin gets a **500**.

Required behaviour: if a solve already exists for that user or team on that
challenge, the endpoint must not create another; it responds with HTTP
**400** (`success: false`) instead of 500 and leaves the solve and fail
counts unchanged.

## Steps to reproduce

Route 2 can be reproduced entirely in the running app (see "Running the app
locally" in `_ORIENTATION.md`):

1. Start the app, complete `/setup` with user mode `users`, and stay logged
   in as the admin.
2. Create a challenge: Admin Panel, Challenges, the plus button. Use any
   name, category, and value; give it a static flag; set its state to
   Visible.
3. Log out, register a player account, and open the challenge from
   `/challenges`.
4. Submit a wrong answer once, then submit the correct flag. The player now
   has one incorrect submission and one solve.
5. Log back in as the admin and open `/admin/submissions/incorrect`. Select
   the player's wrong submission, click the green "Mark submissions correct"
   button, and confirm.
6. The page reloads with no visible change and the submission is still
   incorrect. The browser's network tab shows why:
   `PATCH /api/v1/submissions/1` returned **500**, and the server console
   prints the underlying error:
   `sqlalchemy.exc.IntegrityError: UNIQUE constraint failed:
   solves.challenge_id, solves.user_id`.

Route 1 is a race and is hard to reproduce from the browser: double-clicking
the challenge's Submit button does send two requests a few milliseconds
apart, but the second nearly always arrives after the first has recorded the
solve, takes the existing "already solved" branch, and returns 200. The bug
needs both requests to pass the "already solved?" check before either has
inserted. Reproduce the underlying failure in a test instead: create an
account that already has a solve for a challenge (the `tests/helpers.py`
factories can build that state directly), then drive the challenge plugin's
solve path once more for the same account and challenge, and you get the
same `IntegrityError`. The solve path reads the client IP from the request,
so give your test request context a remote address
(`environ_base={"REMOTE_ADDR": "127.0.0.1"}`); without one it fails in
`get_ip` before reaching the insert.

## Getting started

- `tests/api/v1/test_challenges.py` and `tests/api/v1/test_submissions.py`
  show how both endpoints are driven from tests, and `tests/helpers.py`
  holds the data factories.
- Delete any throwaway reproduction test, or turn it into a real regression
  test, before you submit.

## Acceptance criteria

The names and behaviour below are required exactly.

**New exception**

- A dedicated exception `ChallengeSolveException`, importable as
  `from Tourney.exceptions.challenges import ChallengeSolveException`. This
  exact module path is required.
- A plain `Exception` subclass is sufficient; it must be constructible with a
  single message argument (`ChallengeSolveException("...")`), like the
  neighbouring exception classes in the same module.

**Plugin solve layer (`BaseChallenge.solve`)**

- When inserting the solve violates the unique constraint, `solve()` catches
  the database `IntegrityError`, rolls the session back, and raises
  `ChallengeSolveException` from the caught error (use
  `raise ChallengeSolveException(...) from e`), so the `IntegrityError` is
  preserved as the exception's `__cause__`.
- After the rollback, the original solve row is intact and no second row
  exists.
- This holds in both modes: uniqueness is per `user_id` in users mode and per
  `team_id` in teams mode.

**Attempt endpoint (Route 1)**

- When `solve()` raises `ChallengeSolveException`, the endpoint returns HTTP
  **200** with `success: true`, `data.status == "already_solved"`, and a
  message containing the text `"already solved this"`. No extra solve row is
  created.

**Re-grade endpoint (Route 2)**

- Marking a submission `correct` when a solve already exists for that
  user/team on that challenge returns HTTP **400** with `success: false`,
  creates no solve row, and leaves the solve/fail counts unchanged. No
  specific error message is required.
- The existing submission row is otherwise untouched; do not change its type
  when refusing.
- The existence check keys on the account dimension (`user_id` in users mode,
  `team_id` in teams mode). Both modes must work.

**General**

- The existing test suite still passes.

---

See [README.md](./README.md) for how to work this task: the process, the no-AI rule, keeping _THINKING.md, and how your work is evaluated.
