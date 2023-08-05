/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_GEODESICS_HPP__
#define YAYI_LOWLEVEL_GEODESICS_HPP__


/*!@file
 * This file defines geodesic erosions and dilations
 * @author Raffi Enficiaud
 */



#include <Yayi/core/yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi {
  namespace llmm {

    using namespace yayi::se;
    
    /*!@brief Computes the geodesic dilation of imin inside immask with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC geodesic_dilation(const IImage* imin, const IImage* immask, const IStructuringElement*, IImage* imout);


    /*!@brief Computes the geodesic erosion of imin outside immask with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC geodesic_erosion(const IImage* imin, const IImage* immask, const IStructuringElement*, IImage* imout);
    
  }
}


#endif /* YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__ */
