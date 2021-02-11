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

ns = Collection()

ci = Collection('ci')
ci.add_task(server)
ci.add_task(login)

ns.add_collection(ci)
