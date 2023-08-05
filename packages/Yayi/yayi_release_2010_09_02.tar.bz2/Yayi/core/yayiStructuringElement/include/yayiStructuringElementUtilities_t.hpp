/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_STRUCTURING_ELEMENT_UTILITIES_T_HPP__
#define YAYI_STRUCTURING_ELEMENT_UTILITIES_T_HPP__

/*!@file
 * This file contains some usefull functions for manipulating structuring elements
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>

namespace yayi
{
  namespace se
  {
    
    
    /*! Returns the points of the unit ball shaped by the l_1 metric
     * The ball includes the center
     */
    template <class coordinate_type>
    std::vector<coordinate_type> create_l1_point_list()
    {
      std::vector<coordinate_type> list_points;
      
      coordinate_type current(0);
      list_points.push_back(current);
      for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++)
      {
        current[i] = -1;
        list_points.push_back(current);
        current[i] = 1;
        list_points.push_back(current);
        current[i] = 0;
      }
      
      return list_points;
    }

    /*! Returns a ball shaped by the l_1 metric
     * The ball includes the center
     */
    template <class coordinate_type>
    s_neighborlist_se<coordinate_type> create_l1_ball()
    {
      typedef se::s_neighborlist_se<coordinate_type> ball_t;
      return ball_t(create_l1_point_list<coordinate_type>());
    }
  

    /*! Returns the points of the unit ball shaped by the l_\infty metric
     * The ball includes the center
     */
    template <class coordinate_type>
    std::vector<coordinate_type> create_linfty_point_list()
    {
      static coordinate_type const center(1);
      static coordinate_type const size(3);

      // maybe this one static too ?
      std::vector<coordinate_type> list_points;

      // ballade sur un hypercube de dimension "dimension"
      for(offset o = 0, o_end = total_number_of_points(size); o < o_end; o++)
      {
        list_points.push_back(from_offset_to_coordinate(size, o) - center);
      }
      
      return list_points;
    }


    /*! Returns a ball shaped by the l_\infty metric
     * The ball includes the center
     */
    template <class coordinate_type>
    s_neighborlist_se<coordinate_type> create_linfty_ball()
    {
      typedef se::s_neighborlist_se<coordinate_type> ball_t;
      return ball_t(create_linfty_point_list<coordinate_type>());
    }
  
  
    /*! Returns a list of points directly surrounding the point given as argument 
     * (for instance a "real" points surrounded by the integer grid of the image)
     */
    template <int dim, class T>
    std::vector< s_coordinate<dim> > get_surrounding_points_linfty(const s_coordinate<dim, T>& c)
    {
      typedef s_coordinate<dim> coordinate_o_t;
      std::vector< coordinate_o_t > out;
      
      coordinate_o_t translated;
      for(int i = 0; i < dim; i++)
      {
        translated[i] = static_cast<typename coordinate_o_t::scalar_coordinate_type>(::floor(c[i]));
      }
      
      //const int dimension = c.dimension(); // not necessarilly the dim parameter in case 0
      std::vector<coordinate_o_t> v = create_linfty_point_list<coordinate_o_t>();
      for(unsigned int i = 0; i < v.size(); i++)
      {
        out.push_back(v[i] + translated);
      }
      
      return out;
    }

    //! In case an integer point is given as parameter, we return a list containing only this points (and not the surrouding points)
    template <int dim>
    std::vector< s_coordinate<dim> > get_surrounding_points_linfty(const s_coordinate<dim>& c)
    {
      std::vector< s_coordinate<dim> > out; out.push_back(c); return out;
    }

  
  }



}

#endif /* YAYI_STRUCTURING_ELEMENT_UTILITIES_T_HPP__ */
