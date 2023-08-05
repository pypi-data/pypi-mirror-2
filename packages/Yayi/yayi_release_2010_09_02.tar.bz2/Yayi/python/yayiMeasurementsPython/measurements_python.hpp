/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef MEASUREMENTS_PYTHON_HPP__
#define MEASUREMENTS_PYTHON_HPP__

#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <boost/python/def.hpp>

namespace bpy = boost::python;

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiMeasurements/yayiMeasurements.hpp>

namespace yayi
{
  typedef yaRC (*measurements_function_t)(IImage const*, variant&);
  typedef yaRC (*measurements_on_regions_function_t)(IImage const*, IImage const*, variant&);


  template <measurements_function_t p>
  variant measurements_function(IImage const* imin)
  {
    variant out;
    yaRC res = p(imin, out);
    if(res != yaRC_ok)
      throw errors::yaException(res);
    
    return out;
    
  }
  
  template <measurements_on_regions_function_t p>
  variant measurements_on_regions_function(const IImage* imin, IImage const* imregions)
  {
    variant out;
    yaRC res = p(imin, imregions, out);
    if(res != yaRC_ok)
      throw errors::yaException(res);
    
    return out;
    
  }  
}



#endif
