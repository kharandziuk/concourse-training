from invoke import task, Collection
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CI_NAME = Path().cwd().name


def run(c, cmd):
    """
    a wrapper to simplify debuging
    """
    SIZE = 50
    print("=" * SIZE)
    print(f"-> {cmd} <-")
    print("=" * SIZE)
    result = c.run(cmd)
    print("=" * SIZE)
    print(f"<- {cmd} ->")
    print("=" * SIZE)
    return result


# ci collection
@task
def server(c):
    with c.cd('concourse'):
        run(c, 'docker-compose up -d')


@task(server)
def login(c):
    run(c, f'fly login -t {CI_NAME} -u test -p test -c http://localhost:8080')


@task(login)
def set_pipeline(c, name, secrets=None):
    import json
    if secrets:
        secrets = json.loads(secrets)
    secrets = secrets or {}
    print(secrets)
    params = ' '.join([
        f'-v {k}="{v}"'
        for k, v in secrets.items()
    ])
    run(
        c,
        f"fly -t {CI_NAME} set-pipeline -c ./CI/{name}.yml -p {name} " +
        params
    )


@task
def execute(c):
    run(c, f"fly -t {CI_NAME} execute -i repo=. --config ci/tasks/test.yml")

@task
def test(c):
    run(c, 'python test.py')

@task
def format(c):
    run(c, 'flake8 .')


ns = Collection()
code = Collection('code')

code.add_task(test)

ci = Collection('ci')
ci.add_task(server)
ci.add_task(login)
ci.add_task(execute)
ci.add_task(set_pipeline)

ns.add_collection(ci)
ns.add_collection(code)
