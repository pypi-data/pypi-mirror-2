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
#include "Yayi/core/yayiCommon/include/current_configuration.hpp"
#include "Yayi/core/yayiCommon/include/common_string_utilities.hpp"

#include <ctime>

class build_test 
{
public:

  void test()
  {
    using namespace yayi;
    struct tm null_tm = { 0, 0, 00, 01, 01, 2000 };
    int current_configuration = yayi::current_build_version();
    BOOST_CHECK_MESSAGE(current_configuration != 0, "Current build version cannot be 0");
    struct tm current_build_date = yayi::current_build_date();
    BOOST_CHECK_MESSAGE(
          current_build_date.tm_year  != null_tm.tm_year
      ||  current_build_date.tm_mon   != null_tm.tm_mon
      ||  current_build_date.tm_mday  != null_tm.tm_mday
      ||  current_build_date.tm_hour  != null_tm.tm_hour
      ||  current_build_date.tm_min   != null_tm.tm_min
      ||  current_build_date.tm_sec   != null_tm.tm_sec ,
      "Current build date cannot be 2000/01/01 00:00:00");


    std::cout << "Version info: " << std::endl;
    std::cout << "\tcurrent version : " << current_configuration << std::endl;
    std::cout << "\tLast commit date: " 
      << int_to_string(current_build_date.tm_year, 4) << "/" << int_to_string(current_build_date.tm_mon, 2) << "/" << int_to_string(current_build_date.tm_mday, 2) << " "
      << int_to_string(current_build_date.tm_hour, 2) << ":" << int_to_string(current_build_date.tm_min, 2) << ":" << int_to_string(current_build_date.tm_sec, 2) << std::endl;
  }

};

void register_build_date_test(test_suite*& test)
{
  boost::shared_ptr<build_test> instance( new build_test );

  test->add( BOOST_CLASS_TEST_CASE( &build_test::test, instance ) );
}

