from tasks.tests import *
from tasks.docker import *


@task(pre=[docker_clean])
def clean(ctx):
    '''
    Run all cleanup tasks
    '''
    pass


@task(pre=[test_unit, docker_build, docker_compose_up, test_integration, test_component, docker_compose_stop])
def test(ctx):
    '''
    Run all type of tests and additional required tasks
    '''
    pass
