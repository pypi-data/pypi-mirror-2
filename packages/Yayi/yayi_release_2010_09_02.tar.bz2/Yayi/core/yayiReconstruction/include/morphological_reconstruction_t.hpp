/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_T_HPP__
#define YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_T_HPP__


/*!@file
 * This file contains the main algorithm for morphological reconstruction (openings and closings by)
 *
 */
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageIterator.hpp>

#include <Yayi/core/yayiStructuringElement/include/yayiNeighborhoodStrategy_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

#include <Yayi/core/yayiCommon/common_priority_queues.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>

#include <Yayi/core/yayiLabel/include/yayi_label_extrema_t.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_arithmetics_t.hpp>

#include <Yayi/core/yayiCommon/common_orders.hpp>

namespace yayi
{
  namespace reconstructions
  {
  
  
  
  
    template <class image_out_t, class order_t = std::less<typename image_out_t::pixel_type> >
    struct s_generic_reconstruction_t
    {
      const order_t order_;
      
      s_generic_reconstruction_t() : order_() {}
      s_generic_reconstruction_t(const order_t &o) : order_(o) {}
      
      template <class image_mark_t, class image_mask_t, class se_t>
      yaRC operator()(const image_mark_t& im_mark, const image_mask_t& im_mask, const se_t& se_, image_out_t& imout) const
      {
        image_mark_t imtemp;
        yaRC res = imtemp.set_same(im_mark);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in set_same");
          return res;
        }
        
        res = predicate_images_t(im_mark, im_mask, order_, imtemp);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in predicate of the images");
          return res;
        }

        // need to reverse the order
        typedef s_reverse_order_helper<order_t> reverse_order_t;
        typename reverse_order_t::type reverse_order(reverse_order_t::reverse(order_));
        
        
        typedef yaUINT16 label_type;
        typedef std::vector<std::pair<label_type, std::vector<offset> > > vect_extrema_t;
        vect_extrema_t vect_extrema;
        res = label::image_label_extrema_into_queue_t(imtemp, se_, reverse_order, vect_extrema);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in predicate");
          return res;
        }
        
        
        // no need for temporary
        res = constant_image_t(s_bounds<typename image_out_t::pixel_type, order_t>::min(), imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("Error in image_constant_t");
          return res;
        }        
        
        // push the candidate points into the priority queue
        typedef priority_queue_t<typename image_out_t::pixel_type, offset, typename reverse_order_t::type> pq_t; 
        
        pq_t pq(reverse_order); 
        for(typename vect_extrema_t::const_iterator it(vect_extrema.begin()), ite(vect_extrema.end()); it != ite; ++it)
        {
          for(typename vect_extrema_t::value_type::second_type::const_iterator it1(it->second.begin()), it1e(it->second.end()); it1 != it1e; ++it1)
          {
            pq.insert(imtemp.pixel(*it1), *it1);
          }
        }
        imtemp.FreeImage();

        typedef se::s_runtime_neighborhood<image_out_t const, se_t> neighborhood_t;
        neighborhood_t neighbor(imout, se_.remove_center());
      
        // flood
        while(!pq.empty())
        {
          typename image_out_t::pixel_type min_k = pq.min_key();
          for(typename pq_t::plateau_const_iterator_type p_it(pq.begin_top_plateau()), p_ite(pq.end_top_plateau()); p_it != p_ite; ++p_it)
          {
            const offset o = *p_it;
            typename image_out_t::reference r = imout.pixel(o);
            if(!order_(r, min_k)) // !(r < min_k) <=> (r >= min_k) : current path comes from another "lower priority" path 
              continue;            
            
            r = min_k;
            
            neighbor.center(o);
            
            for(typename neighborhood_t::const_iterator itn(neighbor.begin()), itne(neighbor.end()); itn != itne; ++itn) 
            {
              const offset neigh_o = itn.Offset();
              
              // we flood only "lower" points of imout
              if(!order_(*itn, min_k)) // !(*itn < min_k) <=> (*itn >= min_k) : neighbor already flooded from a higher priority
                continue;
              const typename image_out_t::pixel_type neigh_val = im_mask.pixel(neigh_o);
              pq.insert_buffered((order_(min_k, neigh_val) ? min_k:neigh_val), neigh_o);
            }
          }
          
          pq.pop_top_plateau();
        
        }
        
        return yaRC_ok;
      
      }
    };
    
    
    
    template <class image_mark_t, class image_mask_t, class se_t, class image_out_t>
    yaRC opening_by_reconstruction_t(const image_mark_t& image_mark, const image_mask_t& image_mask, const se_t& se, image_out_t& image_out)
    {
      s_generic_reconstruction_t<image_out_t> op;
      return op(image_mark, image_mask, se, image_out);
    }
  
    template <class image_mark_t, class image_mask_t, class se_t, class image_out_t>
    yaRC closing_by_reconstruction_t(const image_mark_t& image_mark, const image_mask_t& image_mask, const se_t& se, image_out_t& image_out)
    {
      s_generic_reconstruction_t<image_out_t, std::greater<typename image_out_t::pixel_type> > op;
      return op(image_mark, image_mask, se, image_out);
    }  
  
  }

}


#endif /* YAYI_MORPHOLOGICAL_RECONSTRUCTIONS_T_HPP__ */
