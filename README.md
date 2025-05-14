# DevOps CI/CD Task

## Objective
Build a CI/CD pipeline that lints, tests, builds a Docker image, pushes it to a container registry, and deploys it to a live environment.

## App
- A simple Flask app is provided in `app/`
- The `/healthz` endpoint should return 200 and is used for testing

## Test
- Your pipeline must run `tests/test_app.py` and block deployment if it fails

## Bonus
- Add security scanning, deployment notifications, or infra-as-code setup

## Interview
- You may be given a modified version of the app to validate pipeline robustness
