from invoke import task


@task
def test_unit(ctx):
    '''
    Run all unit tests
    '''
    ctx.run('python -m pytest tests/unit')


@task
def test_integration(ctx):
    '''
    Run all integration tests
    '''
    ctx.run('python -m pytest tests/integration')


@task
def test_component(ctx):
    '''
    Run all component tests
    '''
    ctx.run('python -m pytest tests/component')
