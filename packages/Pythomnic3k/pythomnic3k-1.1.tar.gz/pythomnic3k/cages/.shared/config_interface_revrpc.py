# configuration file for the "reverse RPC" interface through which
# other cages can deliver RPC calls to this cage, even though they
# can't reach this cage directly (think DMZ to LAN call).

config = dict \
(
protocol = "revrpc",  # meta
source_cages = (),    # revrpc, names of cages to poll
)

# self-tests of protocol_revrpc.py depend on the following configuration

self_test_config = dict \
(
source_cages = ("source_cage", ),
)

# DO NOT TOUCH BELOW THIS LINE

__all__ = [ "get", "copy" ]

get = lambda key, default = None: pmnc.config.get_(config, self_test_config, key, default)
copy = lambda: pmnc.config.copy_(config, self_test_config)

# EOF
