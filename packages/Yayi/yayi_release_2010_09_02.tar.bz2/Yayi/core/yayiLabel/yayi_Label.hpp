/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_HPP__
#define YAYI_LABEL_HPP__


#include <Yayi/core/yayiCommon/common_config.hpp>

#ifdef YAYI_EXPORT_LABEL_
#define YLab_ MODULE_EXPORT
#else
#define YLab_ MODULE_IMPORT
#endif

#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>

namespace yayi
{
  namespace label
  {

    //! Connected components labelling with a single "id" per connected component in the output image
    YLab_ yaRC ImageLabel(const IImage* imin, const se::IStructuringElement* se, IImage* imout);
    
  }
}

#endif /* YAYI_LABEL_HPP__ */ 
