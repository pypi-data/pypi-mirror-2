/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_LEVELING_HPP__
#define YAYI_MORPHOLOGICAL_LEVELING_HPP__

#include <Yayi/core/yayiReconstruction/yayiReconstruction.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace reconstructions
  {
  
    /*! Morphological leveling
     *
     * @author Raffi Enficiaud
     */
    YRec_ yaRC leveling_by_double_reconstruction(const IImage* im_marker, const IImage* im_mask, const se::IStructuringElement* se, IImage* imout);
  
  }
}


#endif /* YAYI_MORPHOLOGICAL_LEVELING_HPP__ */

