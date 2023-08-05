/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__


/*!@file
 * This file defines opening and closing/closure functions
 * @author Raffi Enficiaud
 */



#include <Yayi/core/yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi {
  namespace llmm {

    using namespace yayi::se;
    
    /*!@brief Computes the open of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC open(const IImage* imin, const IStructuringElement*, IImage* imout);


    /*!@brief Computes the closure of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC close(const IImage* imin, const IStructuringElement*, IImage* imout);
    
  }
}


#endif /* YAYI_LOWLEVEL_MORPHOLOGY_OPENCLOSE_HPP__ */
