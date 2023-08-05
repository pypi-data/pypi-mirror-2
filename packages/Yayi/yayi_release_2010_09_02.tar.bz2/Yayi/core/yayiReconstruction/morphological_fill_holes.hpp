/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__
#define YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__

#include <Yayi/core/yayiReconstruction/yayiReconstruction.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace reconstructions
  {
    //! Fills the holes of imin using the structuring element se, stores the output in imout.
    YRec_ yaRC fill_holes(const IImage* imin, const se::IStructuringElement* se, IImage* imout);
  }
}
 
#endif /* YAYI_MORPHOLOGICAL_FILL_HOLES_HPP__ */
