/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>


namespace yayi { namespace se {
  
  IConstNeighborhood* NeighborListCreate(const IImage& im, const IStructuringElement& se);

  
  IConstNeighborhood* IConstNeighborhood::Create(const IImage& im, const IStructuringElement& se) {
  
    switch(se.GetType()) {
    
    case e_set_neighborlist:
      return NeighborListCreate(im, se);
    
    default:
      YAYI_THROW("Undefined se type requested");
      return 0;
    }
  
  }


}}
