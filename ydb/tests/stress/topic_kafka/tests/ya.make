PY3TEST()
INCLUDE(${ARCADIA_ROOT}/ydb/tests/harness_dep.inc)

TEST_SRCS(
    test_workload_topic.py
)

SIZE(MEDIUM)
REQUIREMENTS(ram:32 cpu:8)

PEERDIR(
    ydb/tests/library
    ydb/tests/library/stress
    ydb/tests/stress/topic_kafka/workload
)


END()
