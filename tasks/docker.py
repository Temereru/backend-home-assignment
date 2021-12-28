from invoke import task


@task
def docker_build(ctx):
    """
    Build the application docker image
    """
    ctx.run('docker build -f docker/Dockerfile . -t app')


@task
def docker_clean(ctx):
    """
    Clean all existing containers and dangling entities
    """
    ctx.run("docker rm -f $(docker ps -aq)", warn=True)
    ctx.run("docker system prune -f")


@task
def docker_compose_up(ctx):
    """
    Start the all containers defined in the tests/docker-compose/docker-compose.yaml file
    """
    ctx.run("docker-compose -f docker/docker-compose.yaml up -d")


@task
def docker_compose_stop(ctx):
    """
    Start the all containers defined in the tests/docker-compose/docker-compose.yaml file
    """
    ctx.run("docker-compose -f tests/docker-compose/docker-compose.yaml stop")


