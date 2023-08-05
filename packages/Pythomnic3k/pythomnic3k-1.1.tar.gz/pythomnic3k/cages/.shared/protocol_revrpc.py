#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-
###############################################################################
#
# This module contains implementation of a reverse RPC interface, it constantly
# polls the configured source cages using regular RPC and fetches calls to this
# cage. The fetched requests are executed and the result is submitted back to
# the originating source cage. Note that there could only one such source cage
# with any given name, because otherwise the result may be submitted to a wrong
# instance. Multiple instances of the same reverse RPC source cage need to have
# unique names, perhaps like source_cage_1, source_cage_2 etc.
#
# Pythomnic3k project
# (c) 2005-2009, Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under BSD license
#
###############################################################################

__all__ = [ "Interface", "self_test_loopback" ]

###############################################################################

import threading; from threading import current_thread

if __name__ == "__main__": # add pythomnic/lib to sys.path
    import os; import sys
    main_module_dir = os.path.dirname(sys.modules["__main__"].__file__) or os.getcwd()
    sys.path.insert(0, os.path.normpath(os.path.join(main_module_dir, "..", "..", "lib")))

import exc_string; from exc_string import exc_string
import typecheck; from typecheck import typecheck, by_regex, tuple_of
import pmnc.threads; from pmnc.threads import HeavyThread
import pmnc.request; from pmnc.request import fake_request

###############################################################################

valid_cage_name = by_regex("^[A-Za-z0-9_-]{1,32}$")
valid_method_name = by_regex("^[A-Za-z0-9_]{1,32}\\.[A-Za-z0-9_]{1,32}$")

###############################################################################

class Interface: # reverse RPC interface

    @typecheck
    def __init__(self, name: str, *,
                 source_cages: tuple_of(valid_cage_name)):

        self._name = name
        self._source_cages = source_cages
        self._poll = lambda cage: pmnc(cage).reverse_call.poll()
        self._post = lambda cage, request_id, result: pmnc(cage).reverse_call.post(request_id, result)

    name = property(lambda self: self._name)

    # a separate thread is executing the following method for each of the configured source cages

    def _poller_proc(self, source_cage):

        # note that poller thread exits when stopped explicitly and also
        # when the cage is stopped, this way the train of calls to stop
        # the pollers will not block the interface's cease at shutdown

        _stopped = lambda: current_thread().stopped() or pmnc.startup.wait(0.0)

        while not _stopped():
            try:

                request_timeout = pmnc.config_interfaces.get("request_timeout")

                # attach a new fake request to this thread so that
                # network access in RPC call times out properly

                fake_request(timeout = request_timeout)

                # fetch a request from the remote cage and extract
                # the call information from it

                try:
                    rpc_request = self._poll(source_cage)
                except:
                    pmnc.log.error(exc_string())
                    current_thread().stopped(request_timeout)
                    continue

                if rpc_request is None:
                    continue
                elif _stopped():
                    break

                assert rpc_request["target_cage"] == __cage__, "expected call to this cage"
                assert rpc_request["source_cage"] == source_cage, "expected call from {0:s}".format(source_cage)

                module = rpc_request["module"]
                method = rpc_request["method"]
                args = rpc_request["args"]
                kwargs = rpc_request["kwargs"]

                request_dict = rpc_request["request"]
                request_dict["interface"] = "revrpc"
                request_dict["protocol"] = "revrpc"
                auth_tokens = dict(source_cage = source_cage)
                request_dict["parameters"]["auth_tokens"] = auth_tokens

                rpc_request = pmnc.request.from_dict(request_dict, timeout = request_timeout)

                # a new request is being created to process the request and submit its result back,
                # notice that it has deadline identical to the impersonated request's

                request_parameters = dict(auth_tokens = dict())
                request = pmnc.interfaces.begin_request(timeout = rpc_request.remain,
                                                        interface = self._name,
                                                        protocol = "revrpc",
                                                        parameters = request_parameters)

                pmnc.performance.event("interface.{0:s}.request_rate".format(self._name))
                pmnc.log.info("interface {0:s} introduces request {1:s} to execute reverse "
                              "RPC request {2:s} ({3:s}.{4:s}), deadline in {5:.01f} second(s)".\
                              format(self._name, request.unique_id, rpc_request.unique_id,
                                     module, method, request.remain))

                pmnc.interfaces.enqueue(request, self.wu_process_request,
                                        (source_cage, module, method, args, kwargs, rpc_request), {})

            except:
                pmnc.log.error(exc_string())

    # this method is a work unit executed by one of the interface pool threads,
    # it does the processing and submits the result back to the originating cage

    def wu_process_request(self, source_cage, module, method, args, kwargs, rpc_request):
        try:

            # see for how long the request was on the execution queue up to this moment
            # and whether it has expired in the meantime, if it did there is no reason
            # to proceed and we simply bail out

            if pmnc.request.expired:
                raise Exception("processing of request {0:s} was late by {1:.01f} second(s)".\
                                format(pmnc.request.unique_id, pmnc.request.expired_for))

            pending_ms = int(pmnc.request.elapsed * 1000)
            pmnc.performance.sample("interface.{0:s}.pending_time".format(self._name), pending_ms)
            try:

                module_method = "{0:s}.{1:s}".format(module, method)

                pmnc.log.info("request {0:s} becomes reverse RPC request {1:s} and "
                              "enters {2:s}(), deadline in {3:.01f} second(s)".\
                              format(pmnc.request.unique_id, rpc_request.unique_id,
                                     module_method, rpc_request.remain))

                original_request = pmnc.request
                current_thread()._request = rpc_request
                try:

                    with pmnc.performance.timing("interface.{0:s}.processing_time".format(self._name)):
                        try:
                            result = pmnc.__getattr__(module).__getattr__(method)(*args, **kwargs)
                        except:
                            error = exc_string()
                            pmnc.log.error("reverse RPC request {0:s} has failed in {1:s}(): {2:s}".\
                                           format(pmnc.request.unique_id, module_method, error))
                            result = dict(exception = error)
                        else:
                            pmnc.log.info("reverse RPC request {0:s} has returned from {1:s}()".\
                                          format(pmnc.request.unique_id, module_method))
                            result = dict(result = result)

                finally:
                    current_thread()._request = original_request

                pmnc.log.debug("request {0:s} submits result for pending reverse RPC request "
                               "{1:s}".format(pmnc.request.unique_id, rpc_request.unique_id))

                self._post(source_cage, rpc_request.unique_id, result)

            except:
                elapsed_ms = int(pmnc.request.elapsed * 1000)
                pmnc.performance.sample("interface.{0:s}.response_time.failure".\
                                        format(self._name), elapsed_ms)
                pmnc.performance.event("interface.{0:s}.response_rate.failure".\
                                       format(self._name))
                raise
            else:
                elapsed_ms = int(pmnc.request.elapsed * 1000)
                pmnc.performance.sample("interface.{0:s}.response_time.success".\
                                        format(self._name), elapsed_ms)
                pmnc.performance.event("interface.{0:s}.response_rate.success".\
                                       format(self._name))

        except:
            pmnc.log.error(exc_string()) # log and ignore
        finally:
            pmnc.interfaces.end_request(pmnc.request)

    # to start/stop an interface separate poller threads, one per source cage

    def start(self):

        self._pollers = []
        for source_cage in self._source_cages:
            poller = HeavyThread(target = self._poller_proc, args = (source_cage, ),
                                 name = "{0:s}:{1:s}".format(self._name, source_cage))
            self._pollers.append(poller)

        for poller in self._pollers:
            poller.start()

    def cease(self):

        for poller in self._pollers:
            poller.stop()

    def stop(self):

        pass

###############################################################################

def self_test_loopback(*args, **kwargs):

    if pmnc.request.self_test != __name__:
        raise Exception("invalid access to self-test code")

    return args, kwargs, pmnc.request.to_dict()

###############################################################################

def self_test():

    from interlocked_queue import InterlockedQueue
    from time import sleep

    get_queue = InterlockedQueue()
    put_queue = InterlockedQueue()

    cage_queues = {
                  "source_cage": (get_queue, put_queue),
                  }

    def create_interface():
        config = pmnc.config_interface_revrpc.copy()
        ifc = pmnc.interface.create("revrpc", **config)
        ifc._poll = lambda cage: pmnc.request.pop(cage_queues[cage][0])
        ifc._post = lambda cage, request_id, result: cage_queues[cage][1].push((request_id, result))
        return ifc

    ifc = create_interface()
    ifc.start()
    try:

        fake_request(3.0)
        pmnc.request.parameters["FOO"] = "BAR"
        request_dict = pmnc.request.to_dict()

        request = dict(source_cage = "source_cage",
                       target_cage = __cage__,
                       module = __name__,
                       method = "self_test_loopback",
                       args = (1, "foo"),
                       kwargs = { "biz": "baz" },
                       request = request_dict)

        get_queue.push(request)
        request_id, result = put_queue.pop(3.0)
        args, kwargs, request_dict = result["result"]

        assert request_id == pmnc.request.unique_id
        assert args == (1, "foo")
        assert kwargs == { "biz": "baz" }

        request = pmnc.request.from_dict(request_dict)
        assert request.interface == "revrpc"
        assert request.protocol == "revrpc"
        assert request.unique_id == pmnc.request.unique_id
        assert request.parameters["FOO"] == "BAR"
        assert request.parameters["auth_tokens"] == { "source_cage": "source_cage" }
        assert request.expires_in(3.0)

        ###############################

        fake_request(3.0)
        request_dict = pmnc.request.to_dict()
        request_dict["deadline"] = request_dict["deadline"] - 10.0

        request = dict(source_cage = "source_cage",
                       target_cage = __cage__,
                       module = __name__,
                       method = "self_test_loopback",
                       args = (1, "foo"),
                       kwargs = { "biz": "baz" },
                       request = request_dict)

        get_queue.push(request)
        assert put_queue.pop(3.0) is None

        ###############################

        fake_request(3.0)

        get_queue.push("garbage")
        assert put_queue.pop(3.0) is None

    finally:
        ifc.cease()
        ifc.stop()

if __name__ == "__main__": import pmnc.self_test; pmnc.self_test.run()

###############################################################################
# EOF