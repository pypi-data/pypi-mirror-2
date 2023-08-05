# This module contains configuration for the notify.py module.
#
# By configuring a separate retry interface and changing retry_queue below
# you can use that interface for sending messages to the health_monitor.
#
# By increasing messages_to_keep you can have a longer history of messages
# on the performance web page.

config = dict \
(
retry_queue = "retry",   # name of a retried queue to use for sending messages to the health monitor
messages_to_keep = 100,  # number of recent messages to keep in memory and display on the web page
)

# self-tests of notify.py depend on the following configuration

self_test_config = dict \
(
messages_to_keep = 4,
)

# DO NOT TOUCH BELOW THIS LINE

__all__ = [ "get", "copy" ]

get = lambda key, default = None: pmnc.config.get_(config, self_test_config, key, default)
copy = lambda: pmnc.config.copy_(config, self_test_config)

# EOF