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


void register_simple_interface_tests(test_suite*& test);
void register_binary_operators_tests(test_suite*& test);
void register_border_tests(test_suite*& test);
void register_copy_tests(test_suite*& test);
// invocation this_test.exe --log_level=all

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* test_suite_ = BOOST_TEST_SUITE( "Pixel processing tests" );
  register_simple_interface_tests(test_suite_);
  register_binary_operators_tests(test_suite_);
  register_border_tests(test_suite_);
  register_copy_tests(test_suite_);
  return test_suite_;
}
