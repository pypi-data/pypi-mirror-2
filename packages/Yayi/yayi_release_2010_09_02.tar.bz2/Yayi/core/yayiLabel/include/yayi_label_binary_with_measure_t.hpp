/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_BINARY_MEASURE_T_HPP__
#define YAYI_LABEL_BINARY_MEASURE_T_HPP__

/*!@file
 * This file defines some labelling functions on "binary" images (taken as black = false and non-black=true), associated to a measurement on the
 * connected component
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiLabel/include/yayi_label_t.hpp>

namespace yayi
{
  namespace label
  {
  
    template <class image_t> 
    struct s_neighbors_not_background
    {
      bool operator()(typename image_t::pixel_type center, typename image_t::pixel_type neighbor) const
      {
         return neighbor != typename image_t::pixel_type(0);
      }
    };

    template <class pixel_type> 
    struct s_neighbors_not_background_already_filtered
    {
      bool operator()(pixel_type center, pixel_type neighbor) const
      {
         return true;
      }
    };

    template <class image_out_t>
    struct s_finalize_with_labelling_and_area_counting 
      : public s_finalize_component_by_image_labeling<image_out_t>
    {
      typedef s_finalize_with_labelling_and_area_counting<image_out_t> this_type;
      typedef s_finalize_component_by_image_labeling<image_out_t> parent_type;
      
      typedef std::map<typename image_out_t::pixel_type, double> storage_type;
      
      storage_type areas;
      
      s_finalize_with_labelling_and_area_counting(this_type& r) : parent_type(r), areas(r.areas) {}
      s_finalize_with_labelling_and_area_counting(image_out_t& im_out_) : parent_type(im_out_) {}
      
      template <class connected_comp_container, class unconnected_comp_container>
      void operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        typename image_out_t::pixel_type const id = parent_type::operator()(p, pu);
        assert(areas.count(id) == 0);
        areas[id] = p.internal_storage().size();
        return;
      }      
    
    };
    
    
    
    //! Binary image labelling with a single id by connected component, and area returns
    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_binary_label_with_area_t(
      const image_in_t &imin, 
      const se_t& se, 
      image_out_t& imout, 
      std::map<typename image_out_t::pixel_type, double>& areas)
    {
      typedef s_finalize_with_labelling_and_area_counting<image_out_t> finalize_t;
      finalize_t finalizer(imout);
      
      s_image_label<
        image_in_t, 
        se_t, 
        finalize_t, 
        s_filter_non_black<typename image_out_t::pixel_type>,
        s_neighbors_not_background_already_filtered<typename image_out_t::pixel_type>
      > label_op(finalizer);
      
      yaRC res = label_op(imin, se);
      if(res != yaRC_ok)
        return res;
      
      areas = label_op.finalize.areas;
      return res;
    };
  }
}


#endif /* YAYI_LABEL_BINARY_MEASURE_T_HPP__ */
