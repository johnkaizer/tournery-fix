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

## Plan

<!-- After reading, before you change any code.
     - The task restated in your own words.
     - The changes you expect to make, in order, and where you think each one
       goes.
     - For a bug: how you will reproduce it before fixing it.
     - Approaches you considered and rejected, and why.
     - Anything you are deliberately leaving out of scope.
     Plans change. When yours does, leave this section as it is and record the
     change as a Progress log entry. -->

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

### [HH:MM]

### [HH:MM]

### [HH:MM]

### [HH:MM]

### [HH:MM]

## Retrospective

<!-- After you finish. This section is required.
     - The weakest part of your solution, named concretely.
     - Where it could break in production, and what you did not cover.
     - What you would do differently with more time.
     - What surprised you about this codebase or this task.
     - Anything you tried and threw away, and why. -->
