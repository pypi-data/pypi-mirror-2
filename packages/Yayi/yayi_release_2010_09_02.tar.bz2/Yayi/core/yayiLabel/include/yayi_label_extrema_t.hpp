/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_LABEL_EXTREMA_T_HPP__
#define YAYI_LABEL_EXTREMA_T_HPP__

/*!@file
 * This file defines extrema detection in images. It uses the generic version of the 
 * labelling, as explained in the PhD of Raffi Enficiaud.
 * @author Raffi Enficiaud
 */


#include <Yayi/core/yayiLabel/include/yayi_label_t.hpp>

namespace yayi
{
  namespace label
  {
  
    //! Functor indicating whether the current connected component is extremal.
    //! It has the same rational as s_no_post_process_unconnected
    //! @see s_no_post_process_unconnected
    template <class pixel_type, class order_t = std::less<pixel_type> >
    struct s_post_process_extrema
    {
      order_t op_order;
      bool current_is_extrema;
      
      s_post_process_extrema() : current_is_extrema(true) {}
      s_post_process_extrema(const order_t& op_) : op_order(op_), current_is_extrema(true) {}
      
      void reset() throw() 
      {
        current_is_extrema = true;
      }
      
      void operator()(
        const offset o_center, 
        const offset o_neigh,
        typename boost::call_traits<pixel_type>::param_type v_center,
        typename boost::call_traits<pixel_type>::param_type v_neighbor) throw() 
      {
        current_is_extrema &= op_order(v_center, v_neighbor);
      }
    };



    //! Functor labelling the extrema plateaus in the output image
    //! It has the same rational as s_finalize_component_by_image_labeling
    //! @see s_finalize_component_by_image_labeling
    template <
      class image_out_t, 
      class connected_component_id_generator_t = s_id_generator<typename image_out_t::pixel_type> >
    struct s_finalize_extrema_by_image_labeling : s_finalize_component_by_image_labeling<image_out_t, connected_component_id_generator_t>
    {
      typedef s_finalize_extrema_by_image_labeling<image_out_t, connected_component_id_generator_t>   this_type;
      typedef s_finalize_component_by_image_labeling<image_out_t, connected_component_id_generator_t> parent_type;
      
      s_finalize_extrema_by_image_labeling(this_type& r) : parent_type(r) {}
      s_finalize_extrema_by_image_labeling(image_out_t& im_out_) : parent_type(im_out_) {}
      
      template <class connected_comp_container, class unconnected_comp_container>
      void operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        if(pu.current_is_extrema)
        {
          parent_type::operator()(p, pu);
        }
        // other case not needed since the image is reset in the constructor
      }
    
    };


    //! Functor labelling the extrema plateaus and storing them into an internal queue
    //! It has the same rational as s_finalize_component_by_image_labeling
    //! @see s_finalize_component_by_image_labeling
    template <
      class pixel_type, 
      class connected_component_id_generator_t = s_id_generator<pixel_type> 
      >
    struct s_finalize_extrema_by_labelling_into_internal_storage : s_finalize_component_by_internal_storage<pixel_type, connected_component_id_generator_t>
    {
      typedef s_finalize_extrema_by_labelling_into_internal_storage<pixel_type, connected_component_id_generator_t> this_type;
      typedef s_finalize_component_by_internal_storage<pixel_type, connected_component_id_generator_t> parent_type;
      
      s_finalize_extrema_by_labelling_into_internal_storage() : parent_type() {}
      s_finalize_extrema_by_labelling_into_internal_storage(this_type& r) : parent_type(r) {}
      
      template <class connected_comp_container, class unconnected_comp_container>
      void operator()(connected_comp_container& p, unconnected_comp_container& pu)
      {
        if(pu.current_is_extrema)
        {
          parent_type::operator()(p, pu);
        }
      }
    
    };






    /*! Extrema plateaus labelling with a single id by connected component
     * The predicate is called in order to decide if the current plateaus is still an extrema, in the following way
     * still_extrema &= pred(x, neighbor(x)); 
     * where x is a point of the plateau, and neighbor(x) is neighbor point of x which does not belong to the plateau. 
     */
    template <class image_in_t, class se_t, class pred_t, class image_out_t>
    yaRC image_label_extrema_t(const image_in_t &imin, const se_t& se, const pred_t& pred, image_out_t& imout)
    {
      typedef s_finalize_extrema_by_image_labeling<image_out_t> finalize_t;
      typedef s_post_process_extrema<typename image_in_t::pixel_type, pred_t> post_process_unconnected_t;
      finalize_t finalizer(imout);
      
      s_image_label<
        image_in_t, 
        se_t, 
        finalize_t, 
        typename label_default_accept<image_in_t>::type,
        typename label_default_relation<image_in_t>::type,
        s_post_process_connected,
        post_process_unconnected_t
        > label_op(finalizer);
        
      label_op.post_process_unconnected = post_process_unconnected_t(pred);
      
      return label_op(imin, se);    
    };


    //! Extrema plateaus labelling with a single id by connected component and a vector of offset for each connected component.
    //! See @ref image_label_extrema_t for details concerning the predicate.
    template <class image_in_t, class se_t, class pred_t, class label_type>
    yaRC image_label_extrema_into_queue_t(
      const image_in_t &imin, 
      const se_t& se, 
      const pred_t& pred,
      std::vector<std::pair<label_type, std::vector<offset> > > & out_queue)
    {
      typedef s_finalize_extrema_by_labelling_into_internal_storage<label_type> finalize_t;
      typedef s_post_process_extrema<typename image_in_t::pixel_type, pred_t> post_process_unconnected_t;
      
      s_image_label<
        image_in_t, 
        se_t, 
        finalize_t, 
        typename label_default_accept<image_in_t>::type,
        typename label_default_relation<image_in_t>::type,
        s_post_process_connected,
        post_process_unconnected_t
        > label_op;
      
      label_op.post_process_unconnected = post_process_unconnected_t(pred);
      
      yaRC res = label_op(imin, se);
      if(res != yaRC_ok)
        return res;
      
      out_queue.swap(label_op.finalize.internal_storage());
      
      return yaRC_ok;
    };




    //! Minimum plateaus  labelling with a single id by connected component
    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_label_minima_t(const image_in_t &imin, const se_t& se, image_out_t& imout)
    {
      return image_label_extrema_t(imin, se, std::less<typename image_in_t::pixel_type>(), imout);
    };
  

    //! Maximum plateaus labelling with a single id by connected component
    template <class image_in_t, class se_t, class image_out_t>
    yaRC image_label_maxima_t(const image_in_t &imin, const se_t& se, image_out_t& imout)
    {
      return image_label_extrema_t(imin, se, std::greater<typename image_in_t::pixel_type>(), imout);
    };






    //! Minimum labelling with a single id by connected component and a vector of offset for each connected component.
    template <class image_in_t, class se_t, class label_type>
    yaRC image_label_minima_into_queue_t(
      const image_in_t &imin, 
      const se_t& se, 
      std::vector<std::pair<label_type, std::vector<offset> > > & out_queue)
    {    
      return image_label_extrema_into_queue_t(imin, se, std::less<typename image_in_t::pixel_type>(), out_queue);
    };


  
  }
}

#endif /* YAYI_LABEL_EXTREMA_T_HPP__ */
