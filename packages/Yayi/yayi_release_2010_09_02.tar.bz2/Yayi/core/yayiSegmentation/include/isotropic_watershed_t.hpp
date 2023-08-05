/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_ISOTROPIC_WATERSHED_T_HPP__
#define YAYI_ISOTROPIC_WATERSHED_T_HPP__

/*!@file
* This file contains the implementation of the isotropic watershed based on hierarchical queues
* as defined in the PhD thesis of Raffi Enficiaud
* @author Raffi Enficiaud
*/


#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_priority_queues.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>


#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>
#include <Yayi/core/yayiLabel/include/yayi_label_extrema_t.hpp>

// for logging
#ifdef WATERSHED_DEBUG_INFO__ 
	#undef WATERSHED_DEBUG_IM 
  #undef DEBUG_STEP
#endif
#undef WATERSHED_DEBUG_INFO__

#ifndef WATERSHED_DEBUG_INFO__
#define WATERSHED_DEBUG_IM(x)
#define DEBUG_STEP(x)
#else
std::ostream &logger = std::cout;
#define WATERSHED_DEBUG_IM(x) {\
  /*logger << x.Description() << std::endl;*/\
  for(int i = 0; i < x.Size()[1]; i++) {\
    for(int j = 0; j < x.Size()[0]; j++) {\
      logger << (int)x.pixel(x.Size()[0]*i + j) << " ";\
    }\
    logger << std::endl;\
  }}

#define DEBUG_STEP(x) {logger << x << std::endl;}
#endif



namespace yayi { namespace segmentation {



  /*!@brief Seeded (so called "supervised") isotropic watersehd on a topographical map
   *
   * This functor structure implements the isotropic watershed as defined in the PhD thesis of Raffi Enficiaud.
   * @author Raffi Enficiaud
   */
  template <
    class image_topo_map_t, 
    class image_labels_t, 
    class se_t, 
    class ordering = std::less<typename image_topo_map_t::pixel_type>
    >
  struct s_seeded_watershed {
  
  private:
    ordering order_op;

  public:
    
    s_seeded_watershed() : order_op()
    {}
    
    s_seeded_watershed(const ordering& p) : order_op(p)
    {}

    yaRC operator()(
      const image_topo_map_t	&imin,
      const image_labels_t		&imLabels,
      const se_t              &se,
      image_labels_t          &imout) const throw()
    {

      if(!imin.IsAllocated() || !imLabels.IsAllocated() || ! imout.IsAllocated())
      {
        DEBUG_INFO("Some images are unallocated");
        return yaRC_E_not_allocated;
      }

      if(!are_same_geometry(imin, imout) || !are_same_geometry(imin, imLabels))
      {
        DEBUG_INFO("Some images have incompatible offsets");
        return yaRC_E_bad_size;
      }

      typedef typename image_labels_t::pixel_type label_pixel_t;
      typedef typename s_get_same_image_of_t<label_image_pixel_t, image_topo_map_t>::type work_image_t;

      typedef se::s_runtime_neighborhood<image_labels_t const, se_t>  imlabel_neighborhood;
      typedef se::s_runtime_neighborhood<work_image_t, se_t>          imwork_neighborhood;

      yaRC res = copy_image_t(imLabels, imout);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error in copy : " << res);
        return res;
      }
      
      image_topo_map_t work; 
      res = work.set_same(imin);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error while setting the work image : " << res);
        return res;
      }

      res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), work);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error in set_constant : " << res);
        return res;
      }

      // value of the watershed line: to be extracted outside the method (best choice: yayiCommon)
      const label_pixel_t lpeVal(0);
      const label_pixel_t label_background_value(0);

      imlabel_neighborhood neighb(imLabels, se.remove_center());
      imwork_neighborhood	work_neighb(work, se.remove_center());


      typedef priority_queue_t<typename image_topo_map_t::pixel_type, offset, ordering> priority_q_t;
      priority_q_t priority_q(order_op);
      
      typedef std::vector<offset> delay_q_t;
      delay_q_t candidates_to_label, points_queued_possible_conflicting, candidates_to_watershed, candidates_no_label_found;
      
      typedef std::vector< std::pair<offset, label_pixel_t> > delay_q_label_origin_t;
      delay_q_label_origin_t points_to_flood, points_to_queue;
      


      DEBUG_STEP("init");
      DEBUG_STEP("candidate " << (int)e_lab_candidate);
      DEBUG_STEP("processed " << (int)e_lab_processed);
      DEBUG_STEP("queued "    << (int)e_lab_queued);
      DEBUG_STEP("queued2 "   << (int)e_lab_queued2);
      DEBUG_STEP("watershed " << (int)e_lab_watershed);
      WATERSHED_DEBUG_IM(work);
            
      for(typename image_labels_t::const_iterator tmpit(imLabels.begin_block()), tmpit_end(imLabels.end_block()); tmpit != tmpit_end; ++tmpit)
      {
        const label_pixel_t value_center = *tmpit;
        if(value_center == label_background_value) 
          continue;

        neighb.center(tmpit);

        bool b_watershedLine = false;
        
        for(typename imlabel_neighborhood::const_iterator nit = neighb.begin(), nend = neighb.end(); nit != nend; ++nit)
        {
          const offset o = nit.Offset();

          // neighbor label
          label_pixel_t const label_neighbor = imLabels.pixel(o);
          if(label_neighbor != label_background_value)
          {
            if(label_neighbor != value_center)
            {
              b_watershedLine = true;
              break;
            }
          }
          else
          {
            candidates_to_label.push_back(o);
          }
        }

        if(!b_watershedLine)
        {
          work.pixel(tmpit.Offset()) = static_cast<label_image_pixel_t>(e_lab_processed);
          
          for(typename delay_q_t::const_iterator it(candidates_to_label.begin()), ite(candidates_to_label.end()); it != ite; ++it)
          {
            const offset oo = *it;
            // prevents from inserting a point twice
            if(work.pixel(oo) == static_cast<label_image_pixel_t>(e_lab_candidate))
            {
              work.pixel(oo) = static_cast<label_image_pixel_t>(e_lab_queued);
              priority_q.insert(imin.pixel(oo), oo);
              imout.pixel(oo) = value_center;
            }
          }
          candidates_to_label.clear();
        }
        else
        {
          const offset offset_center = tmpit.Offset();
          imout.pixel(offset_center)= lpeVal;
          work.pixel(offset_center)	= static_cast<label_image_pixel_t>(e_lab_watershed);
          candidates_to_label.clear();
        }
        assert(candidates_to_label.empty());
      }
      
      DEBUG_STEP("init end");
      DEBUG_STEP("work ");
      WATERSHED_DEBUG_IM(work);
      DEBUG_STEP("imout ");
      WATERSHED_DEBUG_IM(imout);
      DEBUG_STEP("-----");


      while(!priority_q.empty())
      {
        typename image_topo_map_t::pixel_type const current_priority = priority_q.min_key();
        
        for(typename priority_q_t::plateau_const_iterator_type it_plateau(priority_q.begin_top_plateau()), it_plateau_end(priority_q.end_top_plateau());
            it_plateau != it_plateau_end; 
            ++it_plateau)
        {

          label_pixel_t value_center;
          
          bool b_labelled(false), b_watershedLine(false);

          offset const offset_center = *it_plateau;
          assert(work.pixel(offset_center) != static_cast<label_image_pixel_t>(e_lab_watershed));
          if(work.pixel(offset_center) == static_cast<label_image_pixel_t>(e_lab_queued2))
          {
            b_watershedLine	= true;
          }
          else
          {
            assert(points_queued_possible_conflicting.empty());
            work_neighb.center(offset_center);
            for(typename imwork_neighborhood::const_iterator wit = work_neighb.begin(), wend = work_neighb.end(); wit != wend; ++wit)
            {
              const offset o = wit.Offset();

              label_image_pixel_t const state_point = *wit;
                
              if(state_point == static_cast<label_image_pixel_t>(e_lab_candidate))
              {
                candidates_to_label.push_back(o);
              }
              else if(state_point == static_cast<label_image_pixel_t>(e_lab_processed))
              {
                if(b_labelled)
                {
                  assert(value_center != label_background_value);
                  if(imout.pixel(o) != value_center)
                  {
                    b_watershedLine	= true;
                    break;
                  }
                }
                else
                {
                  value_center = imout.pixel(o);
                  b_labelled = true;
                }
              }
              else if(state_point == static_cast<label_image_pixel_t>(e_lab_queued) || state_point == static_cast<label_image_pixel_t>(e_lab_queued2))
              {
                points_queued_possible_conflicting.push_back(o);

              }
            }

            if(!b_watershedLine)
            {
              for(typename delay_q_t::iterator it = points_queued_possible_conflicting.begin(), ite = points_queued_possible_conflicting.end(); it != ite; ++it)
              {
                const offset o = *it;
                const label_pixel_t weak_label = imout.pixel(o);
                
                if((imout.pixel(offset_center) != weak_label) && (weak_label != label_background_value))
                {

                  if(!order_op(current_priority, imin.pixel(o)))
                  {
                    if(work.pixel(o) != static_cast<label_image_pixel_t>(e_lab_queued2))
                    {
                      work.pixel(o) = static_cast<label_image_pixel_t>(e_lab_queued2);
                      candidates_to_watershed.push_back(o);               
                    }

                    b_watershedLine	= b_labelled = true;
                  }
                }
              }
            }
            points_queued_possible_conflicting.clear();

          }

          if(!b_watershedLine)
          {
            if(!b_labelled)
            {
              candidates_no_label_found.push_back(offset_center);
              candidates_to_label.clear();
            }
            else
            {
              assert(b_labelled);
              points_to_flood.push_back(std::make_pair(offset_center, value_center));
              
              for(typename delay_q_t::const_iterator it(candidates_to_label.begin()), ite(candidates_to_label.end()); it != ite; ++it)
              {
                points_to_queue.push_back(std::make_pair(*it, value_center));
                
              }
              candidates_to_label.clear();
            }
          }
          else
          {
            if(b_labelled)
              candidates_to_watershed.push_back(offset_center);
            candidates_to_label.clear();
          }

          assert(candidates_to_label.empty());
        }
        
        for(typename delay_q_t::const_iterator it(candidates_to_watershed.begin()), ite(candidates_to_watershed.end()); it != ite; ++it)
        {
          offset const o = *it;
          imout.pixel(o) = lpeVal;
          work.pixel(o)  = static_cast<label_image_pixel_t>(e_lab_watershed);
        }
        candidates_to_watershed.clear();


        for(typename delay_q_label_origin_t::const_iterator it(points_to_flood.begin()), ite(points_to_flood.end()); it != ite; ++it)
        {
          const offset o = it->first;
          if(work.pixel(o) == static_cast<label_image_pixel_t>(e_lab_queued))
            work.pixel(o)	= e_lab_processed;
        }
        points_to_flood.clear();

        for(typename delay_q_label_origin_t::const_iterator it(points_to_queue.begin()), ite(points_to_queue.end()); it != ite; ++it)
        {
          const offset o = it->first;
          if(work.pixel(o) == static_cast<label_image_pixel_t>(e_lab_candidate))
          {
            priority_q.insert_buffered(std::max(imin.pixel(o), current_priority, order_op), o);
            work.pixel(o) = static_cast<label_image_pixel_t>(e_lab_queued);
            imout.pixel(o) = it->second;
          }
        }
        points_to_queue.clear();

        DEBUG_STEP("End plateau " << (int)current_priority);
        DEBUG_STEP("work ");
        WATERSHED_DEBUG_IM(work);
        DEBUG_STEP("imout ");
        WATERSHED_DEBUG_IM(imout);


        assert(candidates_to_watershed.empty());
        assert(candidates_to_label.empty());
        assert(points_to_queue.empty());
        assert(points_to_flood.empty());

        priority_q.pop_top_plateau();


      }

      for(typename delay_q_t::const_iterator it(candidates_no_label_found.begin()), ite(candidates_no_label_found.end()); it != ite; ++it)
      {
        const offset o = *it;
        if(work.pixel(o) != static_cast<label_image_pixel_t>(e_lab_processed))
          imout.pixel(o) = lpeVal;
      }
      candidates_no_label_found.clear();


      return yaRC_ok;
    }
  };
  
  
  /*!@brief Isotropic version of the seeded (so called "supervised") watershed 
   *
   * The label image contains the seeds of the flooding.
   *
   * @author Raffi Enficiaud
   */
  template <class image_map_t, class se_t, class image_label_t>
  yaRC isotropic_seeded_watershed_t(const image_map_t &imin, const image_label_t &imLabels, const se_t &se, image_label_t &imout)
  {
    s_seeded_watershed<image_map_t, image_label_t, se_t> op;
    return op(imin, imLabels, se, imout);
  }
  
  
  
  /*!@brief Isotropic version of the unseeded (so called "unsupervised") watershed 
   *
   * The flood is performed from the 
   * @author Raffi Enficiaud
   */  
  template <class image_map_t, class se_t, class image_label_t>
  yaRC isotropic_watershed_t(const image_map_t &imin, const se_t &se, image_label_t &imout)
  {
    image_label_t imlabel_temp;
    yaRC res = imlabel_temp.set_same(imin);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error returned by the label image initialization: " << res);
      return res;
    }
    res = label::image_label_minima_t(imin, se, imlabel_temp);
    if(res != yaRC_ok)
    {
      DEBUG_INFO("Error returned by the minima detection: " << res);
      return res;    
    }
    s_seeded_watershed<image_map_t, image_label_t, se_t> op;
    return op(imin, imlabel_temp, se, imout);
  }  
  

}} // namespace yayi::segmentation



#endif /* YAYI_ISOTROPIC_WATERSHED_T_HPP__ */
