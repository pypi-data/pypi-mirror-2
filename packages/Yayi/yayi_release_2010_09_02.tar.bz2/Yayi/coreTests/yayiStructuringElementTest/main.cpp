/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include "main.hpp"

void register_se_test(test_suite*& test);
void register_se_iterators_recovery_test(test_suite*& test);
void register_se_runtime_test(test_suite*& test);
void register_neighborhood_runtime_test(test_suite*& test);
void register_neighborhood_factory_test(test_suite*& test);

// invocation yayiStructuringElementTest.exe --log_level=all

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* test_se = BOOST_TEST_SUITE( "Structuring Element" );
  register_se_test(test_se);
  register_se_iterators_recovery_test(test_se);
  register_se_runtime_test(test_se);
  register_neighborhood_runtime_test(test_se);
  register_neighborhood_factory_test(test_se);
  return test_se;
}
