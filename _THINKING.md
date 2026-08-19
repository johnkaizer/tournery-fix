# Thinking Log

<!-- Your working notes for this task. Fill this file in AS YOU GO, not at the
     end. Short, rough, honest entries are exactly what we want. Wrong guesses
     and dead ends are valuable: record them and do not delete or rewrite them
     later. See README.md for how this file is evaluated. -->

## Before reading anything

<!-- Do this first, right after cloning, before you read _ORIENTATION.md or
     _TASK.md and before you set up the environment:
     - Replace the [HH:MM] below with the current time, then commit.
     - Optionally add a line or two: what do you expect this task to involve,
       based only on what you have seen so far? It is fine to be wrong.
     Then start reading. -->

### [21:00] Starting

## Reading notes

<!-- Take notes here while you read _ORIENTATION.md and _TASK.md and take your
     first look at the code. Add a timestamped entry per sitting or per file.
     Record:
     - What you read or opened, by file path.
     - What you learned about how the system fits together, and what surprised you.
     - Where you expect the relevant code to live, before you have confirmed it.
     - Anything you looked up outside the repo (docs, search) and what you took
       from it.
     - Open questions you cannot answer yet. -->

### [21:15]

<!-- - Read: README.md (full)
- Learned: setup instructions, test command, code organization details, known issues
-->

### [23:45]

<!-- - Read: _TASK.md (full)
- Learned: two independent bugs:
- Route 1 is a race condition in
  POST /api/v1/challenges/attempt,two POSTs both succeed despite being passed the “already” parameter):
  The admin re-grade is route 2.
  Unconditional INSERT (PATCH /api/v1/submissions/<id>).
- Expected relevant code in: Tourney/plugins/challenges/__init__.py (for
  The Tourney/api/v1/challengeTrial.py (solve endpoint) is the base endpoint.
  Tourney/exceptions/challenges.py for ChallengeSolveException.
- Accepted criteria are precise such as exception name/module path, HTTP codes etc.
  (200 for route 1, 400 for route 2), and the "already solved this" message:
  All the words in the substring have to be spelled exactly as they are in the string, not in the sense.
  How does solve() now recognize you have a question?How does solve() now recognize that you have a question
  - Open question: how does solve() currently key on account (user_id vs
  Need to test models/__init__.py's account_id hybrid property (team_id)
-->

[00:04]

<!-- - Read: _ORIENTATION.md (full)
- Learned: Tourney is a Flask monolith — one package serving server-rendered
  pages and a REST API. The models are passed through the before_request chain of models for the request.
  view/resource -> SQLAlchemy -> Jinja/Marshmallow response.
- Surprised that: get_current_user_attrs() is memoized per-request — a change
  before-request checks in the latter part of the user mid-request are not seen as a user request.
  same cycle. Applies if the bug touches the request-scoped state.
- Data model: Both Challenges and Submissions are single-table polymorphic.
  Entries go into Solve / Fail split. The abstraction over "Account" is.
  When writing to or reading from code that deals with: user-mode vs team-mode (account_id hybrid property)
  solves must be able to execute in both modes.
- Open question: where is BaseChallenge.solve() located and what is the equation it is solving?
  Currently, does it occur when you insert a duplicate? Need to open
  Tourney/plugins/challenges/ next.
-->

## Plan

<!-- Plan

 Task, restated
There are 2 independent ways duplicate Solves rows (and 500s) can occur:
1. Player submission race: If two requests are made correctly, both players pass the "already" test.
   Given that, it would be beneficial to perform a "solved?" check before inserting and when the second one hits the unique.
   constraint and 500s.
2. Admin re-grade: no matter if a submission is correct, it always goes into a Solve,
   Even if there is already such a constraint, hitting the same constraint.
Both must not 500, and both have to have specific required.
behaviour 200/already_solved for route 1, 400 for route 2.

 Things I need to change, in order
1. Tourney/exceptions/challenges.py — add ChallengeSolveException
   Same as (plain Exception subclass, single message arg), but with no input/output parameters.
   The adjacent exceptions in that module.
Wrap the BaseChallenge.solve function in 2. Tourney/plugins/challenges/__init__.py.
   inspects any insert operation that fails due to integrity constraint violation, rolls back the session and raises
   ChallengeSolveException(...) from e.
The attempt endpoint is located in 3. Tourney/api/v1/challenges.py (attempt endpoint).
   Return 200 and display ChallengeSolveException from solve() to the user.
   When the data.status property is "already_solved", the status is true.If data.status is "already_solved", the status property is true.
   "already solved this".
4. Tourney/api/v1/submissions.py (re-grade endpoint) — before inserting a
   Solve on mark-correct (check for account keyed solve)
   If it exists, return 400;
   success: false, do not change the current submission/solve/fail data.

 Before changing my work, how I will copy my work.
- Route 2: reproducible directly in the browser as specified in the repro steps in
  _TASK.md (create challenge, submit wrong then correct as player, then
  When you see the 500, you can be sure that something is wrong and admin will re-grade the wrong submission to correct it — except the
  IntegrityError in the server console.
- Route 1: Not reliably repeatable with a double-click in the browser (task doc)
  confirms this). Instead: get a test by using tests/helpers.py gen_solve
  Drive immediately to "already solved" state directly from the put operation.
  Once more, call BaseChallenge.solve(), this time with the same account/challenge, and expect the same result.Call BaseChallenge.solve() once again for the same account/challenge, and await the same result.
  same IntegrityError. Need environ_base={"REMOTE_ADDR": "127.0.0.1"} on the
  You might need to adjust the context used by test request since solve() uses get_ip() to retrieve the IP address of the client.

 The ideas that were looked at and dismissed.Things that were thought about and ruled out.
Fill in when you've really considered alternatives — e.g., did you consider using a different approach?
Consider a pre-check, instead of catch-IntegrityError? why is catch-and-
or for an upfront exists-check, rewrite and rollback.
given it's a race?]

 Out of scope
Anything you are intentionally not touching (e.g. not addressing another).
any other possible race conditions not involving the Fail-record path,
do not alter the unique constraint [itself] -->

## Progress log

<!-- The largest and most important section. Start it with a note on your
     environment setup: did it work on the first try, what (if anything) went
     wrong, and roughly how long the test suite took.

     Then add a timestamped entry every time you:
     - search or read code to find something: what you searched for, which
       files you opened, what you found, what you ruled out
     - reproduce the bug or confirm how something behaves
     - change code: which files, and why
     - run tests or other commands: what you ran and what happened
     - hit something unexpected, get stuck, or get unstuck
     - make a trade-off, or change direction from your plan

     A few sentences per entry is enough. Always name the files you looked at
     or changed in that step. "Searched for X, expected it in a/b.py, found it
     wired through c/d.py" is exactly the kind of detail we want. Add as many
     entries as you need. -->

### [00:39]

<!--
- System Python version: 3.14.3; Project python version: 3.11 is required. Installed 3.11
  At the same time, create the venv with the command `py -3.11 -m venv .venv`.
- The C accelerator from gevent failed to load the python execute: python serve.py
  (`gevent._gevent_c_hub_local` missing). Tried `--disable-gevent` flag.
  The next failure is: cmarkgfm -> \_cffi_backend missing. Fixed with
  Run the following command to install the cffi package with the new version: `pip install cffi==1.17.1 --only-binary=:all: --force-reinstall`. -->

### [09:02]

<!--
If a player is found to be importing gevent elsewhere, they will be removed from the game.
  --disable-gevent alone wasn't enough to disable gevent: (Tourney/utils/events/__init__.py),
  I had to also install gevent properly, to get the same results as enough.
- If next failures, same pattern, (compiled extension present in wheel but not
  loadable): greenlet ("greenlet._greenlet"), Pillow ("PIL._imaging"),
  Then add them with the version `rpds-py (rpds.rpds, a transitive dep via flask_restx)`.
  jsonschema -> referencing).
- The actual installed binary was inspected to find the root cause.
  A Python 3.14 wheel was installed into: `rpds.cp314-win_amd64.pyd`
  the 3.11 venv, meaning 'pip' was pointing to the wrong interpreter's pip
- Despite activation of the venv, at some point.
It was recommended to use the explicit form of pip install (i.e., python -m pip install) instead of the default command (pip).
- Re-installing the active venv's interpreter in order to force resolution against it.
  the affected packages with `--only-binary=:all: --force-reinstall`..
   -->

### [18:28]

<!--
The next failures were similar: the extension compiled was in the wheel but was not loaded. This has happened so far for Pillow (PIL._imaging), and now for `rpds-py` (rpds.rpds) which is pulled in by `flask_restx → jsonschema → referencing`.

After investigation of the installed binary, I discovered that the root cause was that the binary being used, rpds.cp314-win_amd64.pyd, was a built version of Python 3.14 in a virtual environment using Python 3.11. Thus, `pip` had been resolving the wrong Python install, despite the venv being activated.

I solved this by running `python -m pip` to guarantee packages are installed against the active venv. Then I used --only-binary=:all: --force-reinstall to reinstall packages which were previously installed.

All 5 packages were reinstalled and python serve.py --disable-gevent was able to run successfully. After the Alembic migration, the load of plugins, and the Flask development server now started as usual at `http://127.0.0.1:4000`.
-->

### [23:29]
<!--
I needed a specific and catchable error for cases where an account has already solved the challenge rather that treating it as a generic crash and so I added a ChallengeSolveException function in "challenges.py" file in "Tourney/exceptions/challenges" to achieve this I just copied the existing pattern in the file.

-->

### [00:07]
<!-- 
So if the account has already solved the challenge the database throws a raw IntegrityError and the request crashes, so I updated solve() to handle duplicate solves more graceful and I wrapped the commit in a try/except so that when this happens, we roll back the transaction and raise a more specific ChallengeSolveException instead, while keeping the original error with from e for debugging
 -->
 ### [07:27]
<!-- In Tourney\api\v1\challenges.py there was no error handling, so when two correct submissions came in almost at the same time the second one could hit an IntegrityError and crash with a 500 error. I have wrapped chal_class.solve(...) in a try/except ChallengeSolveException and if the challenge was already solved, return the same already_solved response the file already uses instead of creating a new response . I have also added ChallengeSolveException to the existing import from Tourney.exceptions.challenges -->


 ### [08:04]
<!-- So in Tourney\api\v1\submissions.py , when an admin marks a submission as correct, it would always try to create a new solve() row without checking if the player had already solved the challenge and if they had, the database would hit the unique constrain and the request would return a 500. To fix this I added a check for an existing solve using the account_id and challenge_id before inserting a new on. If a solve already exists, it now returns a 400 with success: false and an error message instead of trying to insert another one, and the original submission stays unchanged and if there is no an existing solve, everything continues as before. So no duplicate solve is created -->

### [10:17]
<!-- I ran python serve.py  and tested the full flow in the browser by logging in as a normal user, finding a challenge, submitting a wrong flag, then submitting the correct flag and logged out. I logged in  in as admin. I then found the wrong submission in the admin panel and tried to re-grade it as correct. Instead of getting a 500 crash, I got the expected error response. I also opened Developer Tools with F12, went to the Network tab, and checked the PATCH request and it returned 400, which shows that the fix works.   -->

### [10:33]
<!-- I added an automated test to make sure this bug does not come back and the test first creates an existing solve for an account, then tries to solve the same challenge again through the real solve() function and checks that raises the new ChallengeSolveException instead of a raw database error. It also checks that the original solve is still in the database after the rollback. -->

### [10:40]
<!-- I ran pytest tests/challenges/test_solve.py -v to make sure my new test passed on its own and yes it passed as expected   -->

## Retrospective

<!-- After you finish. This section is required.
     - The weakest part of your solution, named concretely.
     - Where it could break in production, and what you did not cover.
     - What you would do differently with more time.
     - What surprised you about this codebase or this task.
     - Anything you tried and threw away, and why. -->
