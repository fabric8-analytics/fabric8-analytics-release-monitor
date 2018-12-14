"""Steps for release monitoring tests."""
from behave import given, then


@given('Container is running')
def container_is_running(context):
    """Check if cointainer is running."""
    assert context.release_monitor.status == 'created'


@then('Check container logs for "{count}" received elements from "{registry}"')
def check_container_logs(context, count, registry):
    """Check container logs for messages."""
    event_count = 0
    for e in context.release_monitor.logs(stream=True):
        if "Processing package from {registry}".\
                format(registry=registry) in e.decode('utf-8'):
            event_count = event_count + 1

        if event_count >= int(count):
            break
