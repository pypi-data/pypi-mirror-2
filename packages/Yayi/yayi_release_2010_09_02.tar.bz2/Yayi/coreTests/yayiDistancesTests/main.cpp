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

using namespace boost::unit_test;



// invocation yayiDistancesTests.exe --log_level=all

void register_qd_tests(test_suite*&);
void register_morpho_tests(test_suite*& test);
void register_exact_tests(test_suite*& test);

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* test_distances = BOOST_TEST_SUITE( "Distances tests" );
  register_qd_tests(test_distances);
  register_morpho_tests(test_distances);
  //register_exact_tests(test_distances);
  return test_distances;
}

