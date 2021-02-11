from invoke import task, Collection
from pathlib import Path

CI_NAME = Path().cwd().name


@task
def server(c):
    with c.cd('concourse'):
        c.run('docker-compose up -d')

@task(server)
def login(c):
    c.run(f'fly login -t {CI_NAME} -u test -p test -c http://localhost:8080')

@task
def execute(c):
    c.run(f"fly -t {CI_NAME} execute -i repo=. --config ci/test.yml")

@task
def test(c):
    c.run('python test.py')

ns = Collection()
ns.add_task(test)

ci = Collection('ci')
ci.add_task(server)
ci.add_task(login)
ci.add_task(execute)

ns.add_collection(ci)
