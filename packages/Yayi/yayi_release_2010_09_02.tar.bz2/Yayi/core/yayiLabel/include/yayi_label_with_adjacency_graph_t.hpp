/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_GRAPH_T_HPP__
#define YAYI_LABEL_GRAPH_T_HPP__

/*!@file
 * This file contains a labelling creating an adjacency graph on the connected components
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiLabel/include/yayi_label_t.hpp>
#include <Yayi/core/yayiCommon/include/common_graph.hpp>
#include <boost/unordered_map.hpp>

namespace yayi
{
  namespace label
  {
  
    //! Functor creating an adjacency graph for neighbor connected components
    //! It has the same rational as s_no_post_process_unconnected
    //! @see s_no_post_process_unconnected
    template <class pixel_type>
    struct s_post_process_for_adjacency_graph
    {
      typedef std::vector<offset> container_type;
      typedef typename container_type::const_iterator const_iterator;
      container_type off_neighbors;

      s_post_process_for_adjacency_graph() {}
      
      void reset() throw() 
      {
        off_neighbors.clear();
      }
      
      void operator()(
        const offset , 
        const offset o_neigh,
        typename boost::call_traits<pixel_type>::param_type ,
        typename boost::call_traits<pixel_type>::param_type ) throw() 
      {
        off_neighbors.push_back(o_neigh);
      }
      
      const_iterator begin()  const {return off_neighbors.begin();}
      const_iterator end()    const {return off_neighbors.end();}
      
      container_type& internal_storage() {return off_neighbors;}      
    };
  
  
    
    template <class image_out_t, class graph_out_t>
    struct s_finalize_with_labelling_and_adjacency_graph
      : public s_finalize_component_by_image_labeling<image_out_t>
    {
      typedef s_finalize_with_labelling_and_adjacency_graph<image_out_t, graph_out_t> this_type;
      typedef s_finalize_component_by_image_labeling<image_out_t> parent_type;
      
      graph_out_t graph;
      boost::unordered_map<typename image_out_t::pixel_type, typename graph_out_t::vertex_descriptor> map_vertices;
      //std::vector<offset> postponed_points;
      
      s_finalize_with_labelling_and_adjacency_graph(this_type& r) : parent_type(r), graph(r.graph) {}
      s_finalize_with_labelling_and_adjacency_graph(image_out_t& im_out_) : parent_type(im_out_) {}
      
      template <class connected_comp_container, class unconnected_comp_container>
      void operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        typename image_out_t::pixel_type const id = parent_type::operator()(p, pu);
        typename graph_out_t::vertex_descriptor v = graph.add_vertex(id);

        map_vertices[id] = v;
        for(typename unconnected_comp_container::const_iterator it(pu.begin()), ite(pu.end()); it != ite; ++it)
        {
          typename image_out_t::pixel_type const val_pix = parent_type::im_out.pixel(*it);
          if(val_pix != typename image_out_t::pixel_type(0))
          {
            graph.add_edge(v, map_vertices[val_pix]);
          }
          /*else
          {
            // the neighbor connected component has not yet an assigned label
            postponed_points.push_back(*it);
          }*/
        }
        
        return;
      }

      #if 0
      // Raffi: not needed since the connected components are discovered in an atomic manner
      // if a connected component has not been labeled yet, it means that the current is labeled (the one that has
      // a non labeled connected component), so the connection in the graph will be created when the neighboring 
      // connected component is labeled.
      void postprocess()
      {
        for(std::vector<offset>::const_iterator it(postponed_points.begin()), ite(postponed_points.end());
            it != ite;
            ++it)
        {
          typename image_out_t::pixel_type const val_pix = parent_type::im_out.pixel(*it);
          if(val_pix != typename image_out_t::pixel_type(0))
          {
            DEBUG_ASSERT(map_vertices.count(val_pix) > 0, "Unknown vertice at pixel " << *it);
            graph.add_edge(v, map_vertices[val_pix]);
          }
          else
          {
            std::cout << "A connected component has not been processed yet ? position : " << *it << std::endl;
          }
        }

      }
      #endif
    
    };
  
    //! Binary image labelling with a single id by connected component, and graph returns
    template <class image_in_t, class se_t, class graph_out_t, class image_out_t>
    yaRC image_label_with_adjacency_graph_t(
      const image_in_t &imin, 
      const se_t& se, 
      image_out_t& imout, 
      graph_out_t& graph)
    {
      typedef s_finalize_with_labelling_and_adjacency_graph<image_out_t, graph_out_t> finalize_t;
      finalize_t finalizer(imout);
      
      s_image_label<
        image_in_t, 
        se_t, 
        finalize_t,
        typename label_default_accept<image_in_t>::type,
        typename label_default_relation<image_in_t>::type,
        s_post_process_connected,
        s_post_process_for_adjacency_graph<typename image_in_t::pixel_type>
      > label_op(finalizer);
      
      yaRC res = label_op(imin, se);
      if(res != yaRC_ok)
        return res;
      
      graph = label_op.finalize.graph;
      return res;
    };  
  
  
  }
}

#endif /* YAYI_LABEL_GRAPH_T_HPP__ */
