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


// invocation yayiIOTests.exe --log_level=all


void register_io_raw_test(test_suite*& test);
void register_io_jpeg_test(test_suite*& test);
void register_io_png_test(test_suite*& test);
#ifdef YAYI_IO_HDF5_ENABLED__
void register_io_hdf5_test(test_suite*& test);
#endif

// creates the test suite
boost::unit_test::test_suite* init_unit_test_suite( int /*argc*/, char* /*argv*/[] ) 
{
  test_suite* tests = BOOST_TEST_SUITE( "IO Core" );
  register_io_raw_test(tests);
  register_io_jpeg_test(tests);
  register_io_png_test(tests);
  
  #ifdef YAYI_IO_HDF5_ENABLED__
    register_io_hdf5_test(tests);
  #endif
  
  return tests;
}

