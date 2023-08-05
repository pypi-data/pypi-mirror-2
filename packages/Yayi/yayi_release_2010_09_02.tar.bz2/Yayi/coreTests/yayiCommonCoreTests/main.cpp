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


// invocation yayiImageCoreTests.exe --log_level=all


void register_coordinate_lifetime_test(test_suite*& test);
void register_types_and_variant_lifetime_test(test_suite*& test);
void register_build_date_test(test_suite*& test);
void register_dispatch_test(test_suite*& test);
void register_priority_queue_test(test_suite*& test);
void register_graph_test(test_suite*& test);

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* test_common_core = BOOST_TEST_SUITE( "Common Core" );
  register_coordinate_lifetime_test(test_common_core);
  register_types_and_variant_lifetime_test(test_common_core);
  register_build_date_test(test_common_core);
  register_dispatch_test(test_common_core);
  register_priority_queue_test(test_common_core);
  register_graph_test(test_common_core);
  return test_common_core;
}

