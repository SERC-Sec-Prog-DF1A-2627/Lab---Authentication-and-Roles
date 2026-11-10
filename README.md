# Secure Authentication, Authorisation and Session Management - Block 1: Authentication and role permissions

Level 6 · Secure Authentication, Authorisation and Session Management · w/c 9 November 2026

Start with [STUDENT-GUIDE.md](STUDENT-GUIDE.md). It includes setup, explanations, all exercises, diagrams, expected results and troubleshooting. Keep answers in [EVIDENCE.md](EVIDENCE.md).

This is an independent two-hour block. Use Python 3.14 in this repository's Codespace. The starter deliberately contains unfinished security tasks; the smoke test should pass, but some security tests should fail until you complete the exercises. Keep forwarded port 5000 private.

```bash
source .venv/bin/activate
python -m pytest -q tests/test_smoke.py
python -m flask --app app run --host 0.0.0.0 --port 5000
```

If setup has not run, use `bash scripts/bootstrap.sh` first. The full instructions explain account details and safe reset commands.

## Completion criteria

- Complete the policy/exploration evidence and labelled coding tasks.
- Add the student test and remove its skip marker.
- Run the entire suite and explain a permitted case and a denied case.
- Complete the final Level 6 evaluation in your own words.
- Commit, push and submit using your classroom50 assignment's collection method.

Supplied tests give formative feedback; they are not a substitute for explaining the policy. No live identity service or real student data is involved.
