/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__
#define YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__

#include <Yayi/core/yayiLowLevelMorphology/include/neighbor_operators_traits_t.hpp>

namespace yayi
{

  template <class op_t, class op_trait_t = struct neighborhood_operator_traits::classical_operator>
  struct s_operator_adapter_to_neighborhood_op
  {
  
    typedef op_trait_t operator_traits; 
    typedef typename op_t::result_type result_type;
    
    op_t op;
    
    s_operator_adapter_to_neighborhood_op() : op() {}
    s_operator_adapter_to_neighborhood_op(op_t const & op_) : op(op_) {}

    template <class iter_t>
    result_type operator()(iter_t it, iter_t const ite)
    {
      op.clear_result();
      for(; it != ite; ++it)
      {
        op(*it);
      }
      return op.result();
    }
  
  };


}


#endif /* YAYI_NEIGHBORHOOD_PROCESSING_OPERATORS_ADAPTERS_HPP__ */
