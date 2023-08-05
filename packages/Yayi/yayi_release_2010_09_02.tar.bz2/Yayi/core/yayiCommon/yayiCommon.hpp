/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_MAIN_HPP__
#define YAYI_COMMON_MAIN_HPP__

#include <Yayi/core/yayiCommon/common_config.hpp>




#ifdef YAYI_EXPORT_COMMON_
#define YCom_ MODULE_EXPORT
#else
#define YCom_ MODULE_IMPORT
#endif

namespace yayi
{


  //! Returns the number of processor units, which is used for parallelization of the computings
  YCom_ unsigned int& NbProcessorUnit();

  //! Returns whether the current architecture is little or big endian
  YCom_ extern const bool is_big_endian;
}


#endif

