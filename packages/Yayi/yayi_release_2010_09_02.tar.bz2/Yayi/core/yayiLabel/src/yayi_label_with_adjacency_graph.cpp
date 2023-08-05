/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiLabel/include/yayi_label_with_adjacency_graph_t.hpp>


#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_variantDispatch.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/se_dispatcher.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>
#include <Yayi/core/yayiCommon/include/common_graphDispatch.hpp>

namespace yayi
{
  namespace label
  {
  
  
    yaRC ImageLabelWithAdjacencyGraph(const IImage* imin, const se::IStructuringElement* se, IImage* imout, IGraph& g)
    {
      using namespace dispatcher;

      yaRC return_value;
      yayi::dispatcher::s_dispatcher<yaRC, const IImage*, const se::IStructuringElement*, IImage*, IGraph&> 
        dispatch_object(return_value, imin, se, imout, g);
      
      yaRC res = dispatch_object.calls_first_suitable(
        fusion::vector_tie(
          // 2D
          image_label_with_adjacency_graph_t< Image<yaUINT8>,  se::s_neighborlist_se< s_coordinate<2> >, s_graph<yaUINT16, bool>, Image<yaUINT16>  >
        )
        );

      if(res == yaRC_ok) return return_value;
      return res;
    }
  
  
  }
}
