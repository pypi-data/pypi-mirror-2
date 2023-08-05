/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_NEIGHBOR_STRATEGY_T_HPP__
#define YAYI_NEIGHBOR_STRATEGY_T_HPP__

/*!@file
 * This file contains structures allowing the proper selection of the neighborhood type 
 * in regards to the structuring element type
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

namespace yayi
{
  namespace se
  {
  
  
    //! Main template definition. See partial specialisations
    template <class image_t, class se_t>
    struct s_neighborhood_dispatch
    {
      typedef s_runtime_neighborhood<image_t const, se_t> type;
    };
    
    
    
  
  
  
  }
}



#endif /*  */
