# Standard library imports
import unittest
import sys

# Custom test libraries
import libtest

# Testable libraries
import test_examples
import test_ets
import test_marginal_pool_price
import test_csd
import test_aieslog

loader = unittest.TestLoader()
remote_suites = [
    loader.loadTestsFromModule(test_examples),
    loader.loadTestsFromTestCase(test_marginal_pool_price.TestMarginalPoolPriceServiceBehaviour),
    loader.loadTestsFromModule(test_ets.TestLiveEtsConnection),
]
remote_suites.extend(test_aieslog.remote_suites)
remote_suites.extend(test_csd.remote_suites)

local_suites = [
    loader.loadTestsFromTestCase(test_marginal_pool_price.TestMarginalPoolPrice),
    loader.loadTestsFromTestCase(test_ets.TestDayBlockIt),
    loader.loadTestsFromTestCase(test_ets.TestPoolPrice),
    loader.loadTestsFromTestCase(test_ets.TestAssetList),
]
local_suites.extend(test_csd.local_suites)
local_suites.extend(test_aieslog.local_suites)


if __name__ == '__main__':
    sys.exit(libtest.main(sys.argv[1:], local_suites, remote_suites))
