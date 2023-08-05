/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_BINARY_WITH_MEASURES_HPP__
#define YAYI_LABEL_BINARY_WITH_MEASURES_HPP__


#include <Yayi/core/yayiLabel/yayi_Label.hpp>


namespace yayi
{
  namespace label
  {
    
    //! Non-black connected components with a single "id" per component, "areas" contains the area of each of the detected components
    YLab_ yaRC ImageBinaryLabelArea(const IImage* imin, const se::IStructuringElement* se, IImage* imout, variant& areas);

  }
}

#endif /* YAYI_LABEL_BINARY_WITH_MEASURES_HPP__ */ 
