/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_CURRENT_CONFIGURATION_HPP__
#define YAYI_CURRENT_CONFIGURATION_HPP__


/*!@file
 * Contains utilities for retrieving the current build version the source were built against.
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiCommon/yayiCommon.hpp>
#include <ctime>


namespace yayi
{
  //! Returns the current SVN version
  YCom_ int current_build_version();


  //! Last comit date
  YCom_ struct tm current_build_date();

}



#endif

