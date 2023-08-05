/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MORPHOLOGICAL_DISTANCES_T_HPP__
#define YAYI_MORPHOLOGICAL_DISTANCES_T_HPP__

/*!@file
 * This file contains the main template implementaion of the morphological distance, based on queue flooding.
 * @author Raffi Enficiaud
 */

#include <deque>

#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>


namespace yayi
{
  namespace distances
  {
  
  

    
    /*! Simple controller for controlled flooding
     *  This class exposes a simple concept indicating that a pixel can be used as a source for flooding. 
     *  It can be enhanced with the values of the pixels that can be flood, but currently this is enough 
     *  for what we need.
     */
    struct s_simple_distance_controller
    {
      bool is_source_point(const offset) const throw()
      {
        return true;
      }
    };

    /*! Geodesic controller for controlled flooding
     *  This class implements the concept of distance controller (see @ref s_simple_distance_controller) with a control image
     *  indicating the pixels that can be used as source for the flooding process (pixels != 0 in the provided image). 
     */
    template <class image_t>
    struct s_geodesic_distance_controller
    {
      typedef s_geodesic_distance_controller<image_t> this_type;
    
    private:
      const image_t &im;
      this_type& operator=(const this_type&);
      
    public:
      s_geodesic_distance_controller(const image_t& im_) : im(im_) {}
      s_geodesic_distance_controller(const this_type& r_) : im(r_.im) {}
      
      bool is_source_point(const offset o) const throw()
      {
        return im.pixel(o) != 0;
      }
    };

 
    /*! Template implementation of the morphological distance transform
     *  This function considers each null point as lying into the background, and from which the distance is computed
     *  (for every non null pixel). It starts by detecting the points lying on the interior boundary of the sets of interest.
     *  These boundary points are set to a distance of value 1 from the background. 
     *  It then floods from these points to the points that are not flood using the adjacency graph given by the parameter nl. 
     *  This function does not allocate any additionnal working image.
     *
     * @author Raffi Enficiaud
     *
     */
    template <class image_in_t, class se_t, class flood_controller_t, class image_indic_t>
    yaRC controlled_binary_distance_t(
        const image_in_t  &imin,
        const flood_controller_t controller,
        const se_t        &nl,
        image_indic_t     &indicatrice_ero)
    {

      if(!imin.IsAllocated() || !indicatrice_ero.IsAllocated())
        return yaRC_E_not_allocated;
      
      if(!are_same_geometry(imin, indicatrice_ero))
        return yaRC_E_bad_size;

      yaRC res = constant_image_t(0, indicatrice_ero);
      assert(res == yaRC_ok);

      typename image_in_t::pixel_type const background_color(0);

      typedef se::s_runtime_neighborhood<const image_in_t, se_t>	neighborhood_t;
      neighborhood_t neighborImage1(imin, nl.remove_center());
      
      typename image_indic_t::pixel_type indic = 1;
      
      typedef std::vector<offset> type_list;
      type_list	process_list, process_list2;

      // Init
      for(typename image_in_t::const_iterator it = imin.begin_block(), itend = imin.end_block(); it != itend; ++it)
      {
        typename image_in_t::pixel_type const val_center = *it;
        
        if(val_center == background_color)
          continue;
        
        const offset off = it.Offset();
        if(!controller.is_source_point(off))
          continue;
        
        res = neighborImage1.center(it);
        assert(res == yaRC_ok);

        for(typename neighborhood_t::const_iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
        {
          if(*nit != background_color && controller.is_source_point(nit.Offset()))
            continue;
            
          // we are on an interior boundary point 
          
          // const offset off_neigh = nit.Offset();
          // here indicatrice_ero is used as a work image, and indicates if a pixel is already in the queue
          // but I think the test is useless since off is used only once in the main init loop (see the break)
          //if(controller.can_flood(off_neigh)/* && indicatrice_ero.pixel(off_neigh) != indic*/)
          {
            process_list.push_back(off);
            indicatrice_ero.pixel(off) = indic;
            break;
          }
        }
      }


      while(!process_list.empty())
      {

        #ifndef NDEBUG
        if((indic+1) > std::numeric_limits<typename image_indic_t::pixel_type>::max())
        {
          DEBUG_INFO("overflow on the distance values");
          return yaRC_E_overflow;
        }
        #endif
        
        indic ++;
        
        for( typename type_list::const_iterator itq = process_list.begin(), itqend = process_list.end(); itq != itqend; ++itq)
        {
          const offset off_queue = *itq;
          
          //indicatrice_ero.pixel(off_queue) = indic;
          
          res = neighborImage1.center(off_queue);
          assert(res == yaRC_ok);

          typename neighborhood_t::const_iterator const nitend  = neighborImage1.end();
          typename neighborhood_t::const_iterator nit           = neighborImage1.begin();
          assert(nit != nitend);

          for(; nit != nitend; ++nit)
          {
            typename image_in_t::pixel_type const curr_val = *nit;
            if(curr_val == background_color)
              continue;
            
            const offset n_o = nit.Offset();
            typename image_indic_t::reference ref_p = indicatrice_ero.pixel(n_o);

            if(ref_p == 0)
            {
              ref_p = indic;
              process_list2.push_back(n_o);
            }
          }


        }

        //indic++; // indic is already set to one before the init, so it should be incremented here
        
        process_list.clear();
        process_list.swap(process_list2);
      }

      return yaRC_ok;
    } 

 

    /*! Template implementation of the morphological distance transform
     *  This function considers each null point as lying into the background, and from which the distance is computed
     *  (for every non null pixel).
     *
     */
    template <class image_mask_t, class se_t, class image_indic_t>
    yaRC distance_from_sets_boundary(
        const image_mask_t  &immask,
        const se_t          &nl,
        image_indic_t       &indicatrice_ero)
    {
      return controlled_binary_distance_t(immask, s_simple_distance_controller(), nl, indicatrice_ero);
    }


    /*! Template implementation of the morphological geodesic distance transform
     *  Same as @ref distance_from_set_boundary but with a geodesic constraint.
     *
     */
    template <class image_mask_t, class image_marker_t, class se_t, class image_indic_t>
    yaRC geodesic_distance_from_sets_boundary(
        const image_mask_t    &immask,
        const image_marker_t  &immarker,
        const se_t            &nl,
        image_indic_t         &indicatrice_ero)
    {
      return controlled_binary_distance_t(immask, s_geodesic_distance_controller<image_marker_t>(immarker), nl, indicatrice_ero);
    }



  }
}




#endif /* YAYI_MORPHOLOGICAL_DISTANCES_T_HPP__ */
