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



// invocation yayiImageCoreTests.exe --log_level=all

void register_image_lifetime_test(test_suite*& test);
void register_image_access_test(test_suite*& test);
void register_image_utility_test(test_suite*& test);
void register_image_apply_test(test_suite*& test);
void register_image_iterators_test(test_suite*& test);

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* test_image_core = BOOST_TEST_SUITE( "Image Core" );
  register_image_lifetime_test(test_image_core);
  register_image_access_test(test_image_core);
  register_image_utility_test(test_image_core);
  register_image_iterators_test(test_image_core);
  register_image_apply_test(test_image_core);
  
  //framework::master_test_suite().add( test_image_core );

  return test_image_core;
}

