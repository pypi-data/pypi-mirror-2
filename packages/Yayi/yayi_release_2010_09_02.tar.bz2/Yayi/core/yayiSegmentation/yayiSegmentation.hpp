/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_SEGMENTATION_MAIN_HPP__
#define YAYI_SEGMENTATION_MAIN_HPP__

/*!@file
 * Main header for the segmentation module
 *
 */

#include <Yayi/core/yayiCommon/common_config.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

#ifdef YAYI_EXPORT_SEGMENTATION_
#define YSeg_ MODULE_EXPORT
#else
#define YSeg_ MODULE_IMPORT
#endif


namespace yayi
{
  namespace segmentation
  {
  
    //! Performs the watershed transform of the input imin map into the output imout
    YSeg_ yaRC isotropic_watershed(const IImage * imin, const se::IStructuringElement* se, IImage* imout);

    //! Performs the watershed transform of the input imin map into the output imout, starting from the seeds defined in imseeds
    YSeg_ yaRC isotropic_watershed(const IImage * imin, const IImage* imseeds, const se::IStructuringElement* se, IImage* imout);
  
  
  }
}


#endif /* YAYI_SEGMENTATION_MAIN_HPP__ */
