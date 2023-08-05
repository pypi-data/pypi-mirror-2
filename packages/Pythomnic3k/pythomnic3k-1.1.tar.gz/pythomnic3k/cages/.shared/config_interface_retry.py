# configuration file for retry interface for a queue named "retry"
#
# this retry interface is used for retrying calls enqueued using
# pmnc("somecage", queue = "retry") and xa.pmnc("somecage", queue = "retry")
#
# don't decrease queue_count unless you are sure the persistent queues
# are empty, otherwise the calls queued in the excluded queues will not
# be processed

config = dict \
(
protocol = "retry",        # meta
queue_count = 4,           # maximum number of retried calls scheduled concurrently
retry_interval = 600.0,    # seconds between attempts to execute retried calls
retention_time = 259200.0, # seconds to keep history of successfully executed calls
)

# self-tests of protocol_retry.py depend on the following configuration

self_test_config = dict \
(
retry_interval = 10.0,
retention_time = 30.0,
)

# DO NOT TOUCH BELOW THIS LINE

__all__ = [ "get", "copy" ]

get = lambda key, default = None: pmnc.config.get_(config, self_test_config, key, default)
copy = lambda: pmnc.config.copy_(config, self_test_config)

# EOF
