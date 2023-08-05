/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_LEVELING_T_HPP__
#define YAYI_MORPHOLOGICAL_LEVELING_T_HPP__

/*!@file
 * This file contains the main algorithm for morphological leveling
 *
 */


#include <Yayi/core/yayiReconstruction/include/morphological_reconstruction_t.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_compare_T.hpp>
#include <Yayi/core/yayiCommon/common_orders.hpp>
#include <Yayi/core/yayiLowLevelMorphology/include/lowlevel_erosion_dilation_t.hpp>

namespace yayi
{

  namespace reconstructions
  {
    using namespace yayi::llmm;
  
  
    /*!@brief Generic leveling by double reconstruction, as detailed in the PhD thesis of Christina Gomila (2001)
     * This implementation provides "one" leveling, according to its definition (see for instance 
     * "Morphological Scale-Space Representation with Levelings", Meyer & Paragos, LNCS 1682 (1999) )
     *
     * 
     * @author Raffi Enficiaud
     */
    template <class image_t, class order_t = std::less<typename image_t::pixel_type> >
    struct s_generic_leveling_by_double_reconstruction
    {
    
      const order_t order_;
      s_generic_leveling_by_double_reconstruction() : order_() {}
      s_generic_leveling_by_double_reconstruction(const order_t &o) : order_(o) {}
    
      template <class se_t>
      yaRC operator()(image_t const & im_marker, image_t const& im_mask, se_t const& se, image_t& imout)
      {
        typedef typename image_t::pixel_type pixel_type;
        
        image_t im_temp; 
        yaRC res = im_temp.set_same(im_marker);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in set_same");
          return res;
        }

        res = dilate_image_t(im_marker, se, im_temp);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in dilate_image_t");
          return res;
        }
        
        res = image_compare_iii(im_temp, order_, im_mask, im_temp, im_mask, im_temp);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in image_compare_iii");
          return res;
        }
        
        s_generic_reconstruction_t<image_t, order_t> op_rec_lower;
        res = op_rec_lower(im_temp, im_mask, se, imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in opening_by_reconstruction_t");
          return res;
        }
        
        res = erode_image_t(im_marker, se, im_temp);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in erode_image_t");
          return res;
        }
        
        typedef typename order_traits<order_t>::reverse reverse_order_t;
        reverse_order_t reversed_order(reverse_order(order_));
        res = image_compare_iii(im_mask, order_, im_temp, im_temp, im_mask, im_temp);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in image_compare_iii");
          return res;
        }

        image_t im_temp2; 
        res = im_temp2.set_same(im_mask);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in set_same");
          return res;
        }

        s_generic_reconstruction_t<image_t, reverse_order_t> op_rec_upper;
        res = op_rec_upper(im_temp, im_mask, se, im_temp2);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in opening_by_reconstruction_t");
          return res;
        }
        im_temp.FreeImage();
                
        res = image_compare_iii(im_mask, order_, im_marker, im_temp2, imout, imout);
        if(res != yaRC_ok)
        {
          DEBUG_INFO("An error occured in the image_compare_iii (original order)");
          //return res;
        }        
        return res;
      }

    };
    
    
    template <class image_t, class se_t>
    yaRC leveling_by_double_reconstruction_t(image_t const& immarker, image_t const& immask, se_t const& se, image_t& imout)
    {
      s_generic_leveling_by_double_reconstruction<image_t> op;
      return op(immarker, immask, se, imout);
    }
   
  
  }
}

#endif /* YAYI_MORPHOLOGICAL_LEVELING_T_HPP__ */
