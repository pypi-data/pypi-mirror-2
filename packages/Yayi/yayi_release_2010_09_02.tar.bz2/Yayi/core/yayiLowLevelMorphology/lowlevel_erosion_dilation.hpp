/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_HPP__
#define YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_HPP__


/*!@file
 * This file defines erosion and dilation functions
 * @author Raffi Enficiaud
 */



#include <Yayi/core/yayiLowLevelMorphology/yayiLowLevelMorphology.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi {
  namespace llmm {

    using namespace yayi::se;
    
    /*!@brief Computes the erosion of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC erosion(const IImage* imin, const IStructuringElement*, IImage* imout);


    /*!@brief Computes the dilation of the input image imin, with the structuring element se, and places the
     * results inside imout
     *
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC dilation(const IImage* imin, const IStructuringElement*, IImage* imout);
    

    /*!@brief Computes the Minkowski subtraction of the input image imin, with the structuring element se, and places the
     * results inside imout
     * Minkowski subtraction and erosion differs on the way they handle structuring elements. The erosion is defined as being
     * the Minkowski subtraction with the transposed structuring element.
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC minkowski_subtraction(const IImage* imin, const IStructuringElement*, IImage* imout);

    /*!@brief Computes the Minkowski addition of the input image imin, with the structuring element se, and places the
     * results inside imout
     * See @ref minkowski_subtraction for some remarks. 
     * @see minkowski_subtraction. 
     * @author Raffi Enficiaud
     */
    YLLMM_ yaRC minkowski_addition(const IImage* imin, const IStructuringElement*, IImage* imout);

  }
}


#endif /* YAYI_LOWLEVEL_MORPHOLOGY_ERODIL_HPP__ */
