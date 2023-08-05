/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_EXTREMA_HPP__
#define YAYI_LABEL_EXTREMA_HPP__


#include <Yayi/core/yayiLabel/yayi_Label.hpp>


namespace yayi
{
  namespace label
  {
    
    //! Connected minima plateaus with a single "id" per minimum in the output image
    YLab_ yaRC ImageLabelMinimas(const IImage* imin, const se::IStructuringElement* se, IImage* imout);

    //! Connected maximas plateaus with a single "id" per maximas in the output image
    YLab_ yaRC ImageLabelMaximas(const IImage* imin, const se::IStructuringElement* se, IImage* imout);
  
  }
}

#endif /* YAYI_LABEL_EXTREMA_HPP__ */ 
