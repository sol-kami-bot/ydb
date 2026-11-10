# -*- coding: utf-8 -*-
import pytest

from ydb.tests.library.stress.fixtures import StressFixture
from ydb.tests.stress.topic_kafka.workload import WriteProfile, YdbTopicWorkload


class TestYdbTopicWorkload(StressFixture):
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, base_setup):
        self._cluster_released = False
        gen = self.setup_cluster(
            extra_feature_flags=[
                "enable_topic_compactification_by_key",
            ],
        )
        next(gen)
        try:
            yield
        finally:
            # setup_cluster would stop the cluster again if resumed.
            self._release_cluster()
            gen.close()

    def _release_cluster(self):
        if self._cluster_released:
            return
        self._cluster_released = True
        driver = getattr(self, "driver", None)
        cluster = getattr(self, "cluster", None)
        if driver is not None:
            driver.stop()
        if cluster is not None:
            cluster.stop()

    def test(self):
        workload = YdbTopicWorkload(
            endpoint=self.endpoint,
            database=self.database,
            duration=self.base_duration,
            consumers=2,
            consumer_threads=2,
            partitions=4,
            write_profiles=[
                WriteProfile(0.01, 9000000, 2, "big_record", 1),
                WriteProfile(8000, 45, 1000, "small_record", 10),
                WriteProfile(800, 4096, 1, "medium_record", 10),
            ],
            tables_prefix="topic",
            restart_interval="15s",
            cleanup_policy_compact=True,
        )
        workload.tear_up()
        try:
            workload.start()
            workload.join()
        finally:
            # Topic cleanup after join only keeps the nodes idle.
            self._release_cluster()
