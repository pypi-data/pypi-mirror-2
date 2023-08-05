/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_PIXEL_PROCESSING_MAIN_HPP__
#define YAYI_PIXEL_PROCESSING_MAIN_HPP__



#include <Yayi/core/yayiCommon/common_config.hpp>


#ifdef YAYI_EXPORT_PIXELPROC_
#define YPix_ MODULE_EXPORT
#else
#define YPix_ MODULE_IMPORT
#endif


namespace yayi
{

  //! Enumerator for comparison operations
  typedef enum e_comparison_operations
  {
    e_co_equal,                 //!< test for equality
    e_co_different,             //!< test for inequality
    e_co_superior,              //!< test if left is superior (or equal) than right
    e_co_superior_strict,       //!< test if left is superior (and inequal) than right
    e_co_inferior,              //!< test if left is inferior (or equal) than right
    e_co_inferior_strict,       //!< test if left is inferior (and inequal) than right
  } comparison_operations;

}


#endif

