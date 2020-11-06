import subprocess

# import sys
from pathlib import Path
import nox  # type: ignore

nox.options.reuse_existing_virtualenvs = True
lint_dependencies = [
    "black==19.10b0",
    "flake8",
    "flake8-bugbear",
    "mypy",
    "check-manifest",
    "packaging>=20.0",
]


@nox.session()
def tests(session):
    session.install("-e", ".", "pytest")
    tests = session.posargs or ["tests"]
    session.run("pytest", *tests)


@nox.session(python="3.8")
def lint(session):
    session.install(*lint_dependencies)
    files = [str(Path("src") / "importation"), "tests"] + [
        str(p) for p in Path(".").glob("*.py")
    ]
    session.run("black", "--check", *files)
    session.run("flake8", *files)
    session.run("mypy", *files)
    session.run("check-manifest")
    session.run("python", "setup.py", "check", "--metadata", "--strict")


@nox.session(python="3.8")
def build(session):
    session.install("setuptools")
    session.install("wheel")
    session.install("twine")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


def has_changes():
    status = (
        subprocess.run(
            "git status --porcelain", shell=True, check=True, stdout=subprocess.PIPE
        )
        .stdout.decode()
        .strip()
    )
    return len(status) > 0


def get_branch():
    return (
        subprocess.run(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )


@nox.session(python="3.8")
def publish(session):
    if has_changes():
        session.error("All changes must be committed or removed before publishing")
    branch = get_branch()
    if branch != "master":
        session.error(f"Must be on 'master' branch. Currently on {branch!r} branch")
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
