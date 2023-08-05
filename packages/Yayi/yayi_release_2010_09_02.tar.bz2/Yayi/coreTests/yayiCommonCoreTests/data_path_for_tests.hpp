/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef COMMON_TESTS_DATA_PATH_HPP__
#define COMMON_TESTS_DATA_PATH_HPP__

#include <string>
#include "boost/filesystem.hpp"

inline std::string get_data_from_data_path(const std::string &filename)
{
  using namespace boost::filesystem;
  path current = path(__FILE__).parent_path();
  path data = current / ".." / "yayiTestData" / filename;
  return data.file_string();

}

#if 0
std::string get_data_path() {

  using boost::filesystem;
  
  path current = path(__FILE__).remove_filename();
  path data = current / ".." / "yayiTestData";
  return data.external_directory_string();
}
#endif

#endif
