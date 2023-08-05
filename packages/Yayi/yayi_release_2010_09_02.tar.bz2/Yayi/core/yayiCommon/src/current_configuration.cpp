/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/core/yayiCommon/include/current_configuration.hpp>
#include <Yayi/core/yayiCommon/include/common_string_utilities.hpp>
#include <Yayi/core/yayiCommon/src/current_configuration_svn_generated.hpp>

namespace yayi
{

  int current_build_version()
  {
    static const int version = integer_extractor(svn_revision_version, 0, 0);
    return version;
  }

  std::tm current_build_date()
  {
    static const std::tm date = from_string_to_date(svn_revision_date);
    return date;
  }


  static unsigned int processor_unit = 2;
  unsigned int& NbProcessorUnit() {
    return processor_unit;
  }
  
  
  bool is_big_endian_helper()
  {
    yaUINT16 word = 0x0001;
    yaUINT8 *byte = (yaUINT8 *) &word;
    return (byte[0] == 0);
  }
  const bool is_big_endian = is_big_endian_helper();
  
}

