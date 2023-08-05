/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_QUASI_DISTANCES_T_HPP__
#define YAYI_QUASI_DISTANCES_T_HPP__

/*!@file
 * This file contains the original and the optimized version of the Quasi Distance
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiDistances/quasi_distance.hpp>

#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/common_priority_queues.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>

#include <Yayi/core/yayiPixelProcessing/include/image_copy_T.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>

#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>


// for logging
#ifdef QD_PERF_INFO__ 
	#undef QD_PERF_INFO__ 
#endif
#undef QD_PERF_INFO__

#ifndef QD_PERF_INFO__
#define QD_DEBUG_LOG(x)
#define QD_DEBUG_LIST_SIZE(x)
#else
#include <Yayi/core/yayiPixelProcessing/include/image_channels_process_T.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_compare_T.hpp>
#include <Yayi/core/yayiIO/include/yayi_IO.hpp>

std::ostream &logger = std::cout;
#define QD_DEBUG_LIST_SIZE(x) {\
  logger << x.size() << std::endl;\
  static int current = 0;\
  typedef typename s_get_same_image_of_t<pixel8u_3, image_in_t>::type trace_image_t;\
  trace_image_t imtrace;\
  imtrace.set_same(imin);\
  channels_compose_t(imin, imin, imin, imtrace);\
  image_compare_si(imLabelPointErodes1, std::not_equal_to<label_image_pixel_t>(), e_lab_queued, imtrace , pixel8u_3(255, 0, 0), imtrace);\
  IO::writePNG("trace_file_" + int_to_string(current++, 10) + ".png", &imtrace);\
  }
#define QD_DEBUG_LOG(x) {logger << x << std::endl;}
#endif

#include <numeric>
#include <algorithm>
#include <limits>
#include <list>


namespace yayi
{
  namespace distances
  {


    template <class image_in_t, class se_t, class image_indic_t, class image_res_t>
    yaRC quasi_distance_t(
        const image_in_t  &imin,
        const se_t        &nl,
        image_indic_t     &indicatrice_ero,
        image_res_t       &residu_ero)
    {

      if(!imin.IsAllocated() || !indicatrice_ero.IsAllocated() || ! residu_ero.IsAllocated())
        return yaRC_E_not_allocated;
      
      if(!are_same_geometry(imin, indicatrice_ero) || !are_same_geometry(imin, residu_ero))
        return yaRC_E_bad_size;

      image_in_t imtemp1, imtemp2;
      yaRC res = imtemp1.set_same(imin);
      assert(res == yaRC_ok);
      res = imtemp2.set_same(imin);
      assert(res == yaRC_ok);

      typedef typename s_get_same_image_of_t<label_image_pixel_t, image_in_t>::type work_image_t;
      work_image_t imLabelPointErodes1; 
      res = imLabelPointErodes1.set_same(imin);
      assert(res == yaRC_ok);
      
      res = copy_image_t(imin, imtemp1);
      assert(res == yaRC_ok);
      res = copy_image_t(imin, imtemp2);
      assert(res == yaRC_ok);

      res = constant_image_t(0, indicatrice_ero);
      assert(res == yaRC_ok);
      res = constant_image_t(0, residu_ero);
      assert(res == yaRC_ok);

      res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), imLabelPointErodes1);
      assert(res == yaRC_ok);


      typedef se::s_runtime_neighborhood<image_in_t, se_t>	neighborhood_t;

      neighborhood_t neighborImage1(imtemp1, nl.remove_center());
      neighborhood_t neighborImage2(imtemp2, nl.remove_center());
      
      typename image_indic_t::pixel_type indic = 0;
      
      typedef std::vector<offset> type_list;
      type_list	process_list, temporary_list;

      // Init
      QD_DEBUG_LOG("Init");
      for(typename image_in_t::const_iterator it = imin.begin_block(), itend = imin.end_block(); it != itend; ++it)
      {
        const offset off = it.Offset();
        typename image_in_t::pixel_type const val_center = *it;

        res = neighborImage1.center(it);
        assert(res == yaRC_ok);

        for(typename neighborhood_t::const_iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
        {
          if(*nit < val_center)
          {
            imLabelPointErodes1.pixel(off) = static_cast<label_image_pixel_t>(e_lab_queued);
            process_list.push_back(off);
            break;
          }
        }
      }

      QD_DEBUG_LOG("Propagation");
      QD_DEBUG_LIST_SIZE(process_list);

      while(!process_list.empty())
      {

        #ifndef NDEBUG
        if((indic+1) > std::numeric_limits<typename image_indic_t::pixel_type>::max())
        {
          DEBUG_INFO("overflow on the distance values");
          return yaRC_E_overflow;
        }
        #endif

        indic++;
        QD_DEBUG_LOG("Indic = " << indic);
        // Step 1
        QD_DEBUG_LOG("\tStep1");
        typename type_list::const_iterator itq, itqend = process_list.end();

        for(itq = process_list.begin(); itq != itqend; ++itq)
        {
          
          const offset off_queue = *itq;
          assert(imLabelPointErodes1.pixel(off_queue) != static_cast<label_image_pixel_t>(e_lab_candidate));

          imLabelPointErodes1.pixel(off_queue) = static_cast<label_image_pixel_t>(e_lab_candidate);

          neighborImage1.center(off_queue);


          typename neighborhood_t::const_iterator const nitend  = neighborImage1.end();
          typename neighborhood_t::const_iterator nit           = neighborImage1.begin();
          assert(nit != nitend);

          typename image_in_t::pixel_type val_erode(*nit);
          for(++nit; nit != nitend; ++nit)
          {
            typename image_in_t::pixel_type const curr_val = *nit;
            
            if(curr_val < val_erode)
              val_erode = curr_val;
          }

          assert(val_erode  < imtemp2.pixel(off_queue));
          imtemp2.pixel(off_queue) = val_erode ;

          // residue
          typename image_in_t::pixel_type const _current_residu = imtemp1.pixel(off_queue) - val_erode;
          if(_current_residu >= residu_ero.pixel(off_queue))
          {
            residu_ero.pixel(off_queue) = _current_residu;
            indicatrice_ero.pixel(off_queue) = indic;
          }
        }



        // Step 2
        QD_DEBUG_LOG("\tStep2");
        for(itq = process_list.begin(); itq != itqend; ++itq)
        {
          const offset off_queue = *itq;
          typename image_in_t::pixel_type const val_current = imtemp2.pixel(off_queue);
          imtemp1.pixel(off_queue) = val_current;

          neighborImage2.center(off_queue);
          for(typename neighborhood_t::const_iterator nit = neighborImage2.begin(), nitend = neighborImage2.end(); nit != nitend; ++nit)
          {
            const offset curr_off = nit.Offset();
            
            typename image_in_t::pixel_type const val_new = *nit;
            if(val_new > val_current)
            {
              if(imLabelPointErodes1.pixel(curr_off) != static_cast<label_image_pixel_t>(e_lab_queued))
              {
                imLabelPointErodes1.pixel(curr_off) = static_cast<label_image_pixel_t>(e_lab_queued);
                temporary_list.push_back(curr_off);
              }
            }
          }
        }

        process_list.clear();
        process_list.swap(temporary_list);
        QD_DEBUG_LIST_SIZE(process_list);
      }

      return yaRC_ok;
    } 

 

    template <class image_in_t, class se_t, class image_indic_t, class image_res_t>
    yaRC quasi_distance_weighted_t(
        const image_in_t  &imin,
        const se_t        &nl,
        const std::vector<double> v_weights,
        image_indic_t     &indicatrice_ero,
        image_res_t       &residu_ero)
    {

      if(!imin.IsAllocated() || !indicatrice_ero.IsAllocated() || ! residu_ero.IsAllocated())
        return yaRC_E_not_allocated;
      
      if(!are_same_geometry(imin, indicatrice_ero) || !are_same_geometry(imin, residu_ero))
        return yaRC_E_bad_size;

      image_in_t imtemp1, imtemp2;
      yaRC res = imtemp1.set_same(imin);
      assert(res == yaRC_ok);
      res = imtemp2.set_same(imin);
      assert(res == yaRC_ok);

      typedef typename s_get_same_image_of_t<label_image_pixel_t, image_in_t>::type work_image_t;
      work_image_t imLabelPointErodes1; 
      res = imLabelPointErodes1.set_same(imin);
      assert(res == yaRC_ok);
      
      res = copy_image_t(imin, imtemp1);
      assert(res == yaRC_ok);
      res = copy_image_t(imin, imtemp2);
      assert(res == yaRC_ok);

      res = constant_image_t(0, indicatrice_ero);
      assert(res == yaRC_ok);
      res = constant_image_t(0, residu_ero);
      assert(res == yaRC_ok);

      res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), imLabelPointErodes1);
      assert(res == yaRC_ok);


      typedef se::s_runtime_neighborhood<image_in_t, se_t>	neighborhood_t;

      neighborhood_t neighborImage1(imtemp1, nl.remove_center());
      neighborhood_t neighborImage2(imtemp2, nl.remove_center());
      
      typename image_indic_t::pixel_type indic = 0;
      
      typedef std::vector<offset> type_list;
      type_list	process_list, temporary_list;

      // Init
      QD_DEBUG_LOG("Init");
      for(typename image_in_t::const_iterator it = imin.begin_block(), itend = imin.end_block(); it != itend; ++it)
      {
        const offset off = it.Offset();
        typename image_in_t::pixel_type const val_center = *it;

        res = neighborImage1.center(it);
        assert(res == yaRC_ok);

        for(typename neighborhood_t::const_iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
        {
          if(*nit < val_center)
          {
            imLabelPointErodes1.pixel(off) = static_cast<label_image_pixel_t>(e_lab_queued);
            process_list.push_back(off);
            break;
          }
        }
      }

      QD_DEBUG_LOG("Propagation");
      QD_DEBUG_LIST_SIZE(process_list);

      while(!process_list.empty() && (indic < v_weights.size()))
      {

        #ifndef NDEBUG
        if((indic+1) > std::numeric_limits<typename image_indic_t::pixel_type>::max())
        {
          DEBUG_INFO("overflow on the distance values");
          return yaRC_E_overflow;
        }
        #endif

        indic++;

        // Step 1
        QD_DEBUG_LOG("\tStep1");
        typename type_list::const_iterator itq, itqend = process_list.end();

        for(itq = process_list.begin(); itq != itqend; ++itq)
        {
          const offset off_queue = *itq;
          assert(imLabelPointErodes1.pixel(off_queue) != static_cast<label_image_pixel_t>(e_lab_candidate));

          imLabelPointErodes1.pixel(off_queue) = static_cast<label_image_pixel_t>(e_lab_candidate);

          neighborImage1.center(off_queue);


          typename neighborhood_t::const_iterator const nitend  = neighborImage1.end();
          typename neighborhood_t::const_iterator nit           = neighborImage1.begin();
          assert(nit != nitend);

          typename image_in_t::pixel_type val_erode(*nit);
          for(++nit; nit != nitend; ++nit)
          {
            typename image_in_t::pixel_type const curr_val = *nit;
            
            if(curr_val < val_erode)
              val_erode = curr_val;
          }

          assert(val_erode  < imtemp2.pixel(off_queue));
          imtemp2.pixel(off_queue) = val_erode ;

          // residue
          typename image_in_t::pixel_type const _current_residu = static_cast<typename image_in_t::pixel_type>((imtemp1.pixel(off_queue) - val_erode) * v_weights[indic-1]);
          if(_current_residu >= residu_ero.pixel(off_queue))
          {
            residu_ero.pixel(off_queue) = _current_residu;
            indicatrice_ero.pixel(off_queue) = indic;
          }
        }



        // Step 2
        QD_DEBUG_LOG("\tStep2");
        for(itq = process_list.begin(); itq != itqend; ++itq)
        {
          const offset off_queue = *itq;
          typename image_in_t::pixel_type const val_current = imtemp2.pixel(off_queue);
          imtemp1.pixel(off_queue) = val_current;

          neighborImage2.center(off_queue);
          for(typename neighborhood_t::const_iterator nit = neighborImage2.begin(), nitend = neighborImage2.end(); nit != nitend; ++nit)
          {
            const offset curr_off = nit.Offset();
            
            typename image_in_t::pixel_type const val_new = *nit;
            if(val_new > val_current)
            {
              if(imLabelPointErodes1.pixel(curr_off) != static_cast<label_image_pixel_t>(e_lab_queued))
              {
                imLabelPointErodes1.pixel(curr_off) = static_cast<label_image_pixel_t>(e_lab_queued);
                temporary_list.push_back(curr_off);
              }
            }
          }
        }

        process_list.clear();
        process_list.swap(temporary_list);
        QD_DEBUG_LIST_SIZE(process_list);
      }

      return yaRC_ok;
    } 


   
    


    template <class image_in_t, class se_t>
    yaRC QuasiDistanceRegularization_t(
      const image_in_t		&imdistance, 
      const se_t          &nl,
      image_in_t          &imdistanceOut)
    {
    
      if(!are_same_geometry(imdistance, imdistanceOut))
        return yaRC_E_bad_size;
      
      typedef priority_queue_t<typename image_in_t::pixel_type, offset> pq_type;
      typedef typename s_get_same_image_of_t<label_image_pixel_t, image_in_t>::type work_image_t;
      work_image_t imLabelPointErodes1; 
      yaRC res = imLabelPointErodes1.set_same(imdistance);
      assert(res == yaRC_ok);
      
      res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), imLabelPointErodes1);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during constant");
        return res;
      }
      
      res = copy_image_t(imdistance, imdistanceOut);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during copy");
        return res;
      }
      
      typedef se::s_runtime_neighborhood<image_in_t, se_t>	neighborhood_t;
      neighborhood_t neighborImage1(imdistanceOut, nl.remove_center());    


      // Init
      for(typename image_in_t::const_iterator it(imdistance.begin_block()), itend(imdistance.end_block()) ; it != itend; ++it)
      {
        //const offset center_off  = it.Offset();
        typename image_in_t::pixel_type const val1 = *it + 1;  // pour le +1 de lipschitz

        res = neighborImage1.center(it);
        assert(res == yaRC_ok);

        for(typename neighborhood_t::const_iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
        {
          const offset curr_off = nit.Offset();
          if(imdistance.pixel(curr_off) > val1) // val1 = imdistance.pixelFromOffset(off) + 1
          {
            imLabelPointErodes1.pixel(curr_off) = static_cast<label_image_pixel_t>(e_lab_queued);
          }
        }
      }
      
      // propagation
      pq_type pq;

      for(typename image_in_t::const_iterator it(imdistance.begin_block()), itend(imdistance.end_block()); it != itend; ++it)
      {
        const offset off_queue  = it.Offset();
        if(imLabelPointErodes1.pixel(off_queue) != static_cast<label_image_pixel_t>(e_lab_queued))
          continue;

        res = neighborImage1.center(it);
        assert(res == yaRC_ok);

        for(typename neighborhood_t::const_iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
        {
          const offset curr_off = nit.Offset();

          if(imLabelPointErodes1.pixel(curr_off) == static_cast<label_image_pixel_t>(e_lab_candidate))
          {
            typename image_in_t::pixel_type const val1 = imdistance.pixel(curr_off) + 1;
            if(imdistanceOut.pixel(off_queue) > val1)
            {
              pq.insert(val1, off_queue);
              imdistanceOut.pixel(off_queue) = val1;
              //break;
            }
            //break;
          }
        }
      }

      //QD_DEBUG_LIST_SIZE(pq);


      while(!pq.empty())
      {
        typename pq_type::plateau_const_iterator_type itp = pq.begin_top_plateau(), itpe = pq.end_top_plateau();
                    
        typename image_in_t::pixel_type const val_current = pq.min_key() + 1;
                
        for(;itp != itpe; ++itp)
        {
          const offset off_queue = *itp;

          label_image_pixel_t &labTemp = imLabelPointErodes1.pixel(off_queue);
          if(labTemp == static_cast<label_image_pixel_t>(e_lab_processed))
            continue;
          labTemp = static_cast<label_image_pixel_t>(e_lab_processed);
          
          res = neighborImage1.center(off_queue);
          assert(res == yaRC_ok);
          
          for(typename neighborhood_t::iterator nit = neighborImage1.begin(), nitend = neighborImage1.end(); nit != nitend; ++nit)
          {
            typename image_in_t::reference val_new = *nit;
            if(val_new > val_current)
            {
              YAYI_ASSERT(imLabelPointErodes1.pixel(nit.Offset()) != static_cast<label_image_pixel_t>(e_lab_processed), "Impossible configuration")
              pq.insert_buffered(val_current, nit.Offset());
              val_new = val_current;
            }
          }
        }

        pq.pop_top_plateau();

        //QD_DEBUG_LIST_SIZE(pq);
      }
    
      return yaRC_ok;
    }
  
  }

}

#endif /* YAYI_QUASI_DISTANCES_T_HPP__ */
