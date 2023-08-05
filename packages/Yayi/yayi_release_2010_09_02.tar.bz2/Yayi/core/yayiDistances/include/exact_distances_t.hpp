/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_EXACT_DISTANCES_T_HPP__
#define YAYI_EXACT_DISTANCES_T_HPP__

/*!@file
 * This file contains the algorithms for computing the exact distances for images of any dimensions
 * The algorithm is based on hierarchical queue flooding of the original image.
 * It can also easily be extented to distances from a function. On that case, the coordinates of the
 * seeds should be provided. 
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiPixelProcessing/include/image_constant_T.hpp>
#include <Yayi/core/yayiCommon/common_labels.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <Yayi/core/yayiCommon/common_priority_queues.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiStructuringElementUtilities_t.hpp>
#include <boost/unordered_map.hpp>

#include <Yayi/core/yayiDistances/include/distance_operations_t.hpp>
#include <boost/mpl/identity.hpp>
#include <boost/mpl/eval_if.hpp>


#define EXACT_DISTANCE_DEBUG__
//#undef EXACT_DISTANCE_DEBUG__
#define EXACT_DISTANCE_DEBUG_2_
//#undef EXACT_DISTANCE_DEBUG_2_

#ifdef EXACT_DISTANCE_DEBUG__
const std::string directory_out = "/Volumes/Data/superraf/Tmp/exact_distances/";
#include <Yayi/core/yayiIO/include/yayi_IO.hpp>
#endif

#ifdef EXACT_DISTANCE_DEBUG_2_
#include <Yayi/core/yayiCommon/include/common_time.hpp>
const int steps = 1000000;
#endif

namespace yayi
{
  namespace distances
  {

#if 0
    template <class element_type, class distance_type>
    struct greater_first_distance : public std::binary_function<element_type, distance_type, bool>
    {
      bool operator()(const element_type &e, const distance_type & d) const
      {
        return d < e.first;
      }
    };
#endif 
    

    

    /*!
     * @brief Helper structure for computing the distance on images
     * @internal
     */
    template <class source_coordinate_t, class t_store_type>
    struct s_generic_distance_helper
    {

      typedef s_generic_distance_helper<source_coordinate_t, t_store_type> this_type;


      typedef t_store_type compare_distance_type;
      typedef source_coordinate_t coordinate_type;
      typedef std::list<coordinate_type const*> source_list_type;
      typedef std::list<compare_distance_type> source_distance_type;

      source_list_type list_sources;
      source_distance_type list_distances;
      compare_distance_type min_distance;
      bool b_fusion;
      
      
      s_generic_distance_helper() : list_sources(), list_distances(), min_distance(std::numeric_limits<compare_distance_type>::max()), b_fusion(false)
      {}
      
      s_generic_distance_helper(compare_distance_type distance, coordinate_type const* const &source): list_sources(), list_distances(), min_distance(distance), b_fusion(false)
      {
        list_sources.push_back(source);
        list_distances.push_back(distance);
      }

      void add_point_if_not_already_in(compare_distance_type distance, coordinate_type const* const &source)
      {
      
        if(std::find(list_sources.begin(), list_sources.end(), source) == list_sources.end())
        {
          #ifdef EXACT_DISTANCE_DEBUG__
          for(typename source_list_type::const_iterator it = list_sources.begin(), ite = list_sources.end();it != ite;++it)
          {
            if(*it == source)
            {
              std::cout  << std::endl << "s_generic_distance::add_point_if_not_already_in" << std::endl;
              std::cout << "point " << *source << " already exists in the list of points" << std::endl;
              throw errors::yaException("s_generic_distance::add_point_if_not_already_in assertion");
            }
          }
          #endif
          list_sources.push_back(source);
          list_distances.push_back(distance);
        }
      }
      
      void add_points_if_not_already_in(const this_type &r_source)
      {
        typename source_list_type::const_iterator it = r_source.list_sources.begin(), ite = r_source.list_sources.end();
        typename source_distance_type::const_iterator it2 = r_source.list_distances.begin();
        assert(r_source.list_distances.size() == r_source.list_sources.size());
        for(; it != ite; ++it, ++it2)
        {
          add_point_if_not_already_in(*it2, *it);
        }
      }

      void re_init_with(compare_distance_type distance, coordinate_type const* const &source)
      {
        list_sources.clear();
        list_sources.push_back(source);
        list_distances.clear();
        list_distances.push_back(distance);
      }

      void re_init_with(const this_type &r_source)
      {
        list_sources.assign(r_source.list_sources.begin(), r_source.list_sources.end());
        list_distances.assign(r_source.list_distances.begin(), r_source.list_distances.end());
      }

      void add_point(compare_distance_type distance, coordinate_type const *const &source)
      {
        #ifdef EXACT_DISTANCE_DEBUG__
        for(typename source_list_type::const_iterator it = list_sources.begin(), ite = list_sources.end(); it != ite; ++it)
        {
          if(*it == source)
          {
            std::cout  << std::endl << "s_generic_distance::add_point" << std::endl;
            std::cout << "point " << *source << " already exists in the list of points" << std::endl;
            throw errors::yaException("s_generic_distance::add_point assertion");
          }
        }
        #endif
        list_sources.push_back(source);
        list_distances.push_back(distance);
      }

      void remove_elements_from_begining(typename source_list_type::const_iterator ite)
      {
        typename source_distance_type::iterator it2 = list_distances.begin();
        typename source_list_type::iterator it = list_sources.begin();
        for(; it != ite; ++it, ++it2)
        {
          it2 = list_distances.erase(it2);
          it = list_sources.erase(it);
        }
      }
      
      
      void discard_all_above(const compare_distance_type distance)
      {
        typename source_distance_type::iterator it2 = list_distances.begin(), it2e = list_distances.end();
        typename source_list_type::iterator it = list_sources.begin();
        assert(list_distances.size() == list_sources.size());
        for(; it2 != it2e; ++it, ++it2)
        {
          if(*it2 > distance)
          {
            it2 = list_distances.erase(it2);
            it = list_sources.erase(it);
          }
        }
      }
      
      template <class distance_t, class node_coordinate_t>
      bool add_points_conditionnaly(distance_t& d_op, const node_coordinate_t& p_current, const this_type& point_queue_entry_center, const compare_distance_type d_lipchitz_condition)
      {
        typedef compare_distance_type storage_type;
        
        storage_type dist_min_lipchitz = min_distance + d_lipchitz_condition;

        // gets the old sources and computes the new distances. Computes the lowest distance as well
        bool b_need_to_be_filtered = false;
        typename source_list_type::iterator const initial_begin = this->list_sources.begin(), initial_end = this->list_sources.end();
        typename source_list_type::iterator last_good_lipchitz;// = initial_end;
        for(typename source_list_type::const_iterator itl = point_queue_entry_center.list_sources.begin(), itle = point_queue_entry_center.list_sources.end();
            itl != itle;
            ++itl)
        {
          coordinate_type const * const &p_origin = *itl;
          if(std::find(initial_begin, initial_end, p_origin) == initial_end)
          {
            const storage_type dist = d_op(*p_origin, p_current);
            if(dist_min_lipchitz < dist)
              continue;
            
            if(dist < min_distance)
            {
              // new lower bound
              b_need_to_be_filtered = true;
              dist_min_lipchitz  = min_distance = dist;
              dist_min_lipchitz += d_lipchitz_condition;
              last_good_lipchitz = list_sources.end();
            }
            this->add_point(dist, p_origin);
          }
        }
        
        if(b_need_to_be_filtered)
        {
          typename source_list_type::iterator it2 = initial_begin;
          typename source_distance_type::iterator it = list_distances.begin();
          for(; it2 != last_good_lipchitz; ++it, ++it2)
          {
            if(*it > dist_min_lipchitz)
            {
              it2 = list_sources.erase(it2);
              it = list_distances.erase(it);
            }
          }
          
          //this->discard_all_above(dist_min + d_lipchitz_condition);
        }
        
        
        // indicates that the neighbor points priority has been updated
        return b_need_to_be_filtered;
      }

    };
    
    template <class T, bool b = false>
    struct s_eval_helper
    {
      typedef yaF_double type;
    };
    template <class T>
    struct s_eval_helper<T, true>
    {
      typedef typename T::storage_type type;
    };
    
    

    
    
    
    template <class source_container_orig_t, class t_distance_operator, class image_out_t>
    yaRC exact_distance_t(const source_container_orig_t &coords_sources_orig, const t_distance_operator& d_op, image_out_t &im_out)
    {
      typedef typename source_container_orig_t::value_type source_coordinate_t;
      
      //we copy the coordinates into a compact place in memory
      typedef std::vector<source_coordinate_t> source_container_t;
      source_container_t coords_sources(coords_sources_orig.begin(), coords_sources_orig.end());
      
      typedef typename s_get_same_image_of_t<label_image_pixel_t, image_out_t>::type work_image_type;

      #if defined(BOOST_MPL_CFG_NO_HAS_XXX)
      BOOST_STATIC_ASSERT(false);
      #endif
      
      #if 0
      typedef typename boost::mpl::eval_if_c<
        distance_has_storage_tag<t_distance_operator>::value,
        mpl::identity<>,
        mpl::identity<yaF_double> >::type storage_type;
      #endif
      
      // distance operator special storage
      typedef typename s_eval_helper<t_distance_operator, distance_has_storage_tag<t_distance_operator>::value>::type storage_type;
      
      // point queue type
      typedef s_generic_distance_helper<source_coordinate_t, storage_type> source_struct_type;

      
      typedef boost::unordered_map<offset, source_struct_type > point_queue_type;
      typedef priority_queue_t<storage_type, offset> distance_pq_type;
      typedef typename image_out_t::coordinate_type coordinate_type;
      
      yaRC res;
      #ifdef EXACT_DISTANCE_DEBUG_2_
      yayi::time::s_time_elapsed time_init;
      #endif 
      
      
      // building neighborhood/propagation graph
      // D_\infty ball
      // D_1 ball + lipschitz condition
      yaF_double d_lipchitz_condition = 0;
      
      typedef se::s_neighborlist_se<coordinate_type> ball_t;
      ball_t ball(se::create_l1_ball<coordinate_type>());
      source_coordinate_t center(0);
      typename ball_t::storage_type const &ball_points = ball.get_coordinates();
      for(typename ball_t::storage_type::const_iterator it(ball_points.begin()), ite(ball_points.end()); it != ite; ++it)
      {
        d_lipchitz_condition = std::max(d_op(center, *it), d_lipchitz_condition);
      }
      #ifdef EXACT_DISTANCE_DEBUG__
      std::cout << "lipshitz condition : " << d_lipchitz_condition << std::endl;
      #endif
      
      // test
      d_lipchitz_condition /= 2.;
      
      // working image, in order to propagate correctly and quickly the points
      work_image_type work;
      res = work.set_same(im_out);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during set same: " << res);
        return res;
      }
      
      #ifdef EXACT_DISTANCE_DEBUG__
      std::cout << "Size im_out " << im_out.Size() << std::endl;
      std::cout << "Size work " << work.Size() << std::endl;
      std::cout << "Total number of points: " << total_number_of_points(work.Size()) << std::endl;
      #endif

      res = constant_image_t(static_cast<label_image_pixel_t>(e_lab_candidate), work);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during set constant: " << res);
        return res;
      }
      
      res = constant_image_t(std::numeric_limits<typename image_out_t::pixel_type>::max(), im_out);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("Error during set constant: " << res);
        return res;
      }
      
      
      
          
      // neighborhoods
      typedef se::s_runtime_neighborhood<work_image_type, ball_t> w_neigh_type;
      //w_neigh_type w_neighb(work, se::create_l1_ball<coordinate_type>().remove_center());
      w_neigh_type w_neighb(work, ball.remove_center()/*se::create_l1_ball<coordinate_type>().remove_center()*/);
      

      point_queue_type point_queue;

      typedef std::vector<offset> points_queue_type;
      points_queue_type new_points_queue, update_points_queue;
      distance_pq_type distance_pq;

      

      #ifdef EXACT_DISTANCE_DEBUG_2_
      std::cout << "begin 2" << std::endl;
      std::cout << "Init total milliseconds = " << time_init.total_milliseconds() << std::endl;
      yayi::time::s_time_elapsed time_init2;
      #endif 
      
      //const coordinate_type origin(0); //, size_im(source_coordinate_t::from_table(&im_out.Size()[0]));
      for(typename source_container_t::const_iterator it(coords_sources.begin()), it_end(coords_sources.end()); it != it_end; ++it)
      {      
        std::vector<coordinate_type> v(se::get_surrounding_points_linfty(*it));
        
        for(int i = 0, j = v.size(); i < j; i++)
        {
          if(!is_point_inside(im_out.Size(), v[i]))
            continue;
          
          // this does not work with negative coordinates
          const offset offset_center = from_coordinate_to_offset(im_out.Size(), v[i]);
        
          #if 0
          // this does not work with negative coordinates
          // this is not a real neighborhood (which garantie the "insideness" of the neighbor points)
          if(offset_center >= total_number_of_points(work.Size()) || offset_center < 0)
          {
            continue;
          }
          #endif
          
          // computing the distance
          const storage_type dist = d_op(*it, v[i]);         
          if(work.pixel(offset_center) != static_cast<label_image_pixel_t>(e_lab_queued))
          {
            // point is new
            // the first field is the lowest distance for this entry
            assert(point_queue.count(offset_center) == 0);
            point_queue.insert(std::make_pair(offset_center, source_struct_type(dist, &(*it))));
            work.pixel(offset_center) = static_cast<label_image_pixel_t>(e_lab_queued);
            new_points_queue.push_back(offset_center);
            
          }
          else
          {
            // point is already known
            source_struct_type &list_sources = point_queue.at(offset_center);
            
            //point_queue[offset_center].add_points_conditionnaly(d_op, v[i], point_queue_entry_center, d_lipchitz_condition);

#if 1
            const storage_type dist_min_fah = list_sources.min_distance;
            
            // case 0: dist_min_fah + Lipschitz < dist : we can discard this point
            if(dist_min_fah + d_lipchitz_condition < dist)
              continue;
            
            // case 1: dist_min_fah <= dist <= dist_min_fah + d_lipchitz_condition
            // we add the point to the source list


            // no need to change the previous known list, we just append the current point
            // to the list of sources
            if(dist_min_fah <= dist) // second inequality (dist <= dist_min_fah + d_lipchitz_condition) is contained with the previous test
            {
              list_sources.add_point_if_not_already_in(dist, &*it);
            }
            else
            {
              // case 2: dist < dist_min_fah : the old list needs update

              // the minimum distance is updated // d_lipchitz_condition is not a reference, so its cool
              list_sources.min_distance = dist;


              // case 2A : dist + d_lipchitz_condition < dist_min_fah : the whole old list can be safely discarded
              if(dist + d_lipchitz_condition < dist_min_fah)
              {
                // previous distance was too big: we can discard the previous source points
                list_sources.re_init_with(dist, &*it);
              }
              else
              {
                // case 2B : dist < dist_min_fah <= dist + d_lipchitz_condition : the whole list needs to be parsed in order to discard points that do not 
                // satisfy the lipschitz condition
                list_sources.discard_all_above(dist + d_lipchitz_condition);
                list_sources.add_point(dist, &*it);
              }
            }
#endif

          }
        }
      }


      for(typename points_queue_type::const_iterator it = new_points_queue.begin(), ite = new_points_queue.end(); it != ite; ++it)
      {
        const offset off = *it;
        const storage_type distance = point_queue.at(off).min_distance;
        im_out.pixel(off) = distance;
        distance_pq.insert(distance, off);
      }
    
      #ifdef EXACT_DISTANCE_DEBUG_2_
      std::cout << "begin 3" << std::endl;
      std::cout << "Init2 total total_milliseconds = " << time_init2.total_milliseconds() << std::endl;
      #endif
        
      points_queue_type points_to_suppress;
       
      #ifdef EXACT_DISTANCE_DEBUG_2_
      std::cout << "begin 4" << std::endl;
      int current_step = 0;
      bool first_pass = true;
      #endif
      
      
      // main loop
      while(!distance_pq.empty())
      {

        points_to_suppress.clear();
        new_points_queue.clear();
        update_points_queue.clear();

        // creates the list of points to propagate
        const storage_type distance = distance_pq.min_key();

        #ifdef EXACT_DISTANCE_DEBUG__
        static const int mechant_coord_t[] = {22, 44, 8};
        static const double real_sources[] = {7.58543, 40.4209, 5.39501};
        static const coordinate_type mechant_coord = coordinate_type::from_table(mechant_coord_t);
        static const offset mechant_offset = from_coordinate_to_offset(im_out.Size(), mechant_coord);
        #endif
       
        #ifdef EXACT_DISTANCE_DEBUG_2_
        bool trace = current_step++ == steps;
        if(trace)
        {
          if(first_pass)
          {
            std::cout << "current distance " << "\t";
            std::cout << "# of distance elements " << "\t";
            std::cout << "# of elements in pq " << "\t";
            std::cout << "# offsets in associative map " << "\t";
            std::cout << "# total elements in associative map " << "\t";
            std::cout << "time step" << "\t";
            std::cout << "\n";
            first_pass = false;
          }
          
          current_step = 0;
          std::cout << distance << "\t";
          std::cout << distance_pq.number_keys() << "\t";
          std::cout << distance_pq.size() << "\t";
          std::cout << point_queue.size() << "\t";
          long int count = 0;
          for(typename point_queue_type::const_iterator it(point_queue.begin()), ite(point_queue.end()); it != ite; ++it)
          {
            count += it->second.list_sources.size();
          }
          std::cout << count << "\t";
          //std::cout << "\n";
        }
        yayi::time::s_time_elapsed time_current;
        #endif


        for(typename distance_pq_type::plateau_const_iterator_type it(distance_pq.begin_top_plateau()), ite(distance_pq.end_top_plateau()); it != ite; ++it)
        {

          const offset off = *it;
          
          if(work.pixel(off) == static_cast<label_image_pixel_t>(e_lab_processed))
            continue;

          work.pixel(off)   = static_cast<label_image_pixel_t>(e_lab_processed);
          assert(im_out.pixel(off) == distance);
          im_out.pixel(off) = static_cast<typename image_out_t::pixel_type>(distance);
                    
          points_to_suppress.push_back(off);
          //point_queue.erase(off); et ben non justement
        }
        #ifdef EXACT_DISTANCE_DEBUG__
        //IO::writePNG(directory_out + "dist_" + any_to_string(distance, 10) + ".png", &work);
        #endif


        // propagates the points 
        for(typename points_queue_type::const_iterator it = points_to_suppress.begin(), ite = points_to_suppress.end(); it != ite; ++it)
        {
          const offset offset_center = *it;
          //typename point_queue_type::const_iterator const iter_bucket = point_queue.find(offset_center);
          //source_struct_type const &point_queue_entry_center = iter_bucket->second;
          source_struct_type const &point_queue_entry_center = point_queue.at(offset_center);
          
          res = w_neighb.center(offset_center);
          DEBUG_ASSERT(res == yaRC_ok, "An error occured during the centering of the structuring element, for offset "  + any_to_string(offset_center) + " res = " + std::string(res));
          for(typename w_neigh_type::iterator nitw(w_neighb.begin()), nendw(w_neighb.end()); nitw != nendw; ++nitw)
          {
            label_image_pixel_t &state_neighbor = *nitw;        // pas besoin de recalculer l'offset ???
            if(state_neighbor == e_lab_processed)
              continue;
            
            const offset off = nitw.Offset();
            assert(off != offset_center); // if this line assert, then it means that the neighboring graph was not properly set (it includes the center)

            coordinate_type const &p_current = nitw.Position();


            
            if(state_neighbor == e_lab_candidate)
            {
              
              // creates the new points lists (pairs<distances, source>)
              assert(point_queue.count(off) == 0);
              source_struct_type& output_filtered_sources = point_queue[off];

              // minimal distances created on p_current by the sources of offset_center
              storage_type dist_min = std::numeric_limits<storage_type>::max();
              storage_type dist_min_plus_lipchitz = std::numeric_limits<storage_type>::max();

              // gets the old sources and computes the new distances. Computes the lowest distance as well
              for(typename source_struct_type::source_list_type::const_iterator itl = point_queue_entry_center.list_sources.begin(), itle = point_queue_entry_center.list_sources.end();
                itl != itle;
                ++itl)
              {
                source_coordinate_t const * const &p_origin = *itl;
                const storage_type dist = d_op(*p_origin, p_current);

                if(dist <= dist_min_plus_lipchitz)
                {
                  // less data to process
                  output_filtered_sources.add_point(dist, p_origin);
                }
                dist_min_plus_lipchitz = dist_min = std::min(dist, dist_min);
                dist_min_plus_lipchitz+= d_lipchitz_condition;
             
                // we do not filter yet, we filter once we know the minimal distance
              }
              
              // best filter in this case is this
              output_filtered_sources.discard_all_above(dist_min_plus_lipchitz);
            
              // append the result to the queue
              output_filtered_sources.min_distance = dist_min;
              
              // mark it as queued
              state_neighbor = e_lab_queued;

              // plans it for distance_pq insert
              new_points_queue.push_back(off);

              #ifdef EXACT_DISTANCE_DEBUG_3_
              if(off == mechant_offset)
              {
                std::cout << "Méchant offset ici : distance = "  << output_filtered_sources.min_distance << "\tsources sont:" << std::endl;
                std::cout << std::for_each(output_filtered_sources.list_sources.begin(), output_filtered_sources.list_sources.end(), s_any_to_string_for_container()).s << std::endl;
                
                std::cout << "Current scope for real source is maybe:" << std::endl;
                for(typename point_queue_type::const_iterator it(point_queue.begin()), ite(point_queue.end()); it != ite; ++it)
                {
                   for(typename source_struct_type::source_list_type::const_iterator itl = it->second.list_sources.begin(), itle = it->second.list_sources.end();
                       itl != itle;
                       ++itl)
                   {
                     
                     if(std::abs((**itl)[0] - real_sources[0]) < 1E-3 && std::abs((**itl)[1] - real_sources[1]) < 1E-3 && std::abs((**itl)[2] - real_sources[2]) < 1E-3)
                     {
                        std::cout << from_offset_to_coordinate(im_out.Size(), it->first) << "\t";
                     }
                   }
                 }
                 std::cout << std::endl << "End current scope for real source" << std::endl;
              }
              #endif

            }
            else// if(c_state_neighbor == e_lab_queued)
            {
              // gets the previous result
              assert(point_queue.count(off) != 0);
              if(point_queue[off].add_points_conditionnaly(d_op, p_current, point_queue_entry_center, d_lipchitz_condition))
              {
                update_points_queue.push_back(off);
              }
              #ifdef EXACT_DISTANCE_DEBUG_3_
              if(off == mechant_offset)
              {
                std::cout << "Méchant offset update : distance = "  << point_queue[off].min_distance << "\tsources sont:" << std::endl;
                std::cout << std::for_each( point_queue[off].list_sources.begin(),  point_queue[off].list_sources.end(), s_any_to_string_for_container()).s << std::endl;
                
                std::cout << "Current scope for real source is maybe:" << std::endl;
                for(typename point_queue_type::const_iterator it(point_queue.begin()), ite(point_queue.end()); it != ite; ++it)
                {
                   for(typename source_struct_type::source_list_type::const_iterator itl = it->second.list_sources.begin(), itle = it->second.list_sources.end();
                       itl != itle;
                       ++itl)
                   {
                     if(std::abs((**itl)[0] - real_sources[0]) < 1E-3 && std::abs((**itl)[1] - real_sources[1]) < 1E-3 && std::abs((**itl)[2] - real_sources[2]) < 1E-3)
                     {
                        std::cout << from_offset_to_coordinate(im_out.Size(), it->first) << "\t";
                     }
                   }
                 }
                 std::cout << std::endl << "End current scope for real source" << std::endl;

                
              }
              #endif
            }


          } // for each neighbor
          
          // we erase the entry here, so we don't need to look for it twice
          // there is no aliasing on the elements of the front since they are in the processed state
          // and we only consider new or queued points
          //point_queue.erase(iter_bucket); 
          // Raffi : false: there is an insert
          
        } // for the lowest plateau

        // suppresses the top plateau (the one we just processed)

        distance_pq.pop_top_plateau();

        


        // suppresses the processed points

        for(typename points_queue_type::const_iterator it = points_to_suppress.begin(), ite = points_to_suppress.end(); it != ite; ++it)
        {
          point_queue.erase(*it); 
        }

        #ifdef EXACT_DISTANCE_DEBUG_2_
        //if(trace)
        //  std::cout << "removing " << points_to_suppress.size() << " elements" << std::endl;
        #endif

        // appends the new points into the distance priority queue
        for(typename points_queue_type::const_iterator it = update_points_queue.begin(), ite = update_points_queue.end(); it != ite; ++it)
        {
          const offset off = *it;
          assert(point_queue.count(off) > 0);
          const storage_type dist = point_queue.at(off).min_distance;
          distance_pq.insert(dist, off);
          im_out.pixel(off) = dist;
        }

        for(typename points_queue_type::const_iterator it = new_points_queue.begin(), ite = new_points_queue.end(); it != ite; ++it)
        {
          const offset off = *it;
          assert(point_queue.count(off) > 0);
          const storage_type dist = point_queue.at(off).min_distance;
          
          // this is the minimal distance anyway, so at worst we insert twice the same point at the same priority
          // which is filtered out by the poping of the queue
          distance_pq.insert(dist, off); 
          im_out.pixel(off) = dist;
        #if 0
          typename image_out_t::reference ref_pix = im_out.pixel(off);
          if(dist < ref_pix)
          {
            distance_pq.insert(dist, off);
            ref_pix /*im_out.pixel(off)*/= dist;
          }
        #endif
        }
        
        #ifdef EXACT_DISTANCE_DEBUG_2_
        if(trace)
          std::cout << time_current.total_microseconds() << "\t";
        #endif
        
        if(trace)
          std::cout << "\n";

      } // while !fah.empty()
      
      return yaRC_ok;
    }
    
    


    /*!@brief Generic exact distance on images of any dimension, with any distance having a convex unit ball
     *
     * @author Raffi Enficiaud
     */
    template <class image_t, class t_distance_operator, class image_out_t>
    yaRC exact_distance_image_t(const image_t &im_in, const t_distance_operator& d_op, image_out_t &im_out)
    {
      BOOST_STATIC_ASSERT(t_distance_operator::coordinate_type::static_dimensions == image_t::coordinate_type::static_dimensions);

      if(!im_in.IsAllocated() || !im_out.IsAllocated())
      {
        return yaRC_E_not_allocated;
      }

      // coordinates
      typedef typename image_t::coordinate_type coordinate_type;

      const typename image_t::value_type background = typename image_t::value_type(0);
      
      std::vector<typename image_t::coordinate_type> v_sources;
      for(typename image_t::const_iterator it(im_in.begin_block()), it_end(im_in.end_block()); it != it_end; ++it)
      {
        if(*it != background)
        {
          v_sources.push_back(it.Position());
        }
      }

      return exact_distance_t(v_sources, d_op, im_out);
    }


    
    
    /*!@brief Exact euclidian distance transform on images of any dimension.
     *
     * Special case of @ref exact_distance_image_t with the euclidian unit distance. 
     * @author Raffi Enficiaud
     */    
    template <class image_t, class image_out_t>
    yaRC euclidian_distance_t(const image_t &im_in, image_out_t &im_out)
    {
      BOOST_DEBUG_ASSERT((boost::is_same<typename image_t::coordinate_type, typename image_out_t::coordinate_type>::value));
      s_euclidian_distance_op<typename image_t::coordinate_type, typename image_t::coordinate_type> dist_op;
      return exact_distance_t(im_in, dist_op, im_out);
    }


  }
}

#endif /* YAYI_EXACT_DISTANCES_T_HPP__  */
