# -*- coding: utf-8 -*-
import os

import pytest

from common import boot_nbs_cluster

_DEFAULT_TIMEOUT = int(os.environ.get('PYTEST_TIMEOUT') or 60)


@pytest.fixture(scope='session')
def nbs_cluster():
    """One cluster per pytest session (pytest session (per FORK process))."""
    cluster = boot_nbs_cluster()
    try:
        yield cluster
    finally:
        cluster.stop()


def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_closest_marker('timeout') is None:
            item.add_marker(pytest.mark.timeout(_DEFAULT_TIMEOUT, func_only=True))
