/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/yayiImageCoreFunctions.hpp>


namespace yayi
{

  IImage* GetSameImage(const IImage* const &im) {
    
    if(im == 0)
      return 0;
    
    yaRC res(yaRC_ok);
    IImage* out = IImage::Create(im->DynamicType(), im->GetDimension());
    out->SetSize(im->GetSize());
    if(im->IsAllocated())
      res = out->AllocateImage();
  
    if(res != yaRC_ok)
      throw errors::yaException(res);
    
    return out;
  
  }
  
  IImage* GetSameImage(const IImage* const &im, const type& t) {
  
    if(im == 0)
      return 0;
    
    if(im->DynamicType() == t)
      return GetSameImage(im);
    
    yaRC res(yaRC_ok);
    IImage* out = IImage::Create(t, im->GetDimension());
    out->SetSize(im->GetSize());
    if(im->IsAllocated())
      res = out->AllocateImage();
  
    if(res != yaRC_ok)
      throw errors::yaException(res);
        
    return out;
  }

}

