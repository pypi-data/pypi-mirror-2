/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_COORDINATES_OPERATIONS_HPP__
#define YAYI_COMMON_COORDINATES_OPERATIONS_HPP__

#include <list>
#include <iterator>
#include <set>
#include <boost/type_traits/is_same.hpp>
#include <boost/static_assert.hpp>
#include <Yayi/core/yayiCommon/common_coordinates.hpp>
#include <Yayi/core/yayiCommon/common_hyperrectangle.hpp>


namespace yayi
{
  
  /*!@brief Returns the transpose of the provided coordinate
   * The origin for the transposition is the point at 0 (on each dimension)
   * @author Raffi Enficiaud
   */
  template <class coordinate>
  coordinate transpose(const coordinate &c) {
		coordinate ret;
    const int j = c.dimension();
		for(int i = 0; i < j; i++)
		{
			ret[i] = -c[i];
		}
    return ret;
  }

  //! In-place transposition (avoiding a copy)
  template <int dim, class T>
  void transpose_in_place(s_coordinate<dim, T> &c) {
		for(int i = 0; i < s_coordinate<dim, T>::static_dimensions; i++)
		{
			c[i] = -c[i];
		}
  }
  
  //! In-place transposition (avoiding a copy)
  template <class T>
  void transpose_in_place(s_coordinate<0, T> &c) {
    const int j = c.dimension();
		for(int i = 0; i < j; i++)
		{
			c[i] = -c[i];
		}
  }
  
  template <class T>
  s_coordinate<0, T> transpose(const s_coordinate<0, T> &c) {
		s_coordinate<0, T> ret(c);
    transpose_in_place(ret);
    return ret;
  }

  template <int dim, class T>
  s_coordinate<dim, T> transpose(const s_coordinate<dim, T> &c) {
		s_coordinate<dim, T> ret;
		for(int i = 0; i < s_coordinate<dim, T>::static_dimensions; i++)
		{
			ret[i] = -c[i];
		}
    return ret;
  }

  /*!@brief Returns the transpose of the provided coordinate relative to a point
   * The origin for the transposition is the point at orig 
   * @author Raffi Enficiaud
   */
  template <class coordinate>
  coordinate transpose(const coordinate &c, const coordinate& orig) {
		coordinate ret;
    const int j = c.dimension();
    DEBUG_ASSERT(c.dimension() == orig.dimension(), "different number of dimensions");
		for(int i = 0; i < j; i++)
		{
			ret[i] = 2*orig[i] - c[i];
		}
    return ret;
  }

  //! Returns a new container of a copy of the transposed elements
  template <class container>
  container transpose_set(const container &c) {
    typedef typename container::value_type coordinate;
    container out;
    for(typename container::const_iterator it(c.begin()), ite(c.end()); it != ite; ++it)
    {
      out.push_back(transpose(*it));
    }
    return out;
  }

  //! In-place transpose
  template <class container>
  void transpose_set_in_place(container &c) {
    std::for_each(c.begin(), c.end(), transpose_in_place<container::value_type::static_dimensions, typename container::value_type::scalar_coordinate_type>);
  }




  /*!@brief Returns true if the given \ref test position is inside the square defined by size (means [0, size[ for each dimension)
   * @author Raffi Enficiaud
   */
  template <class coordinate>
  bool is_point_inside(const coordinate& size, const coordinate& test) {
    if(test[0] < 0 || test[0] >= size[0])
      return false;
    for(unsigned int i = 1, j = size.dimension(); i < j; i++) {
      if(test[i] < 0 || test[i] >= size[i])
        return false;
    }
    return true;
  }

  //! Specialization of @ref is_point_inside for abstract dimensional coordinates
  inline bool is_point_inside(const s_coordinate<0>& size, const s_coordinate<0>& test) {
    for(unsigned int i = 0, j = size.dimension(); i < j; i++) {
      if(test[i] < 0 || test[i] >= size[i])
        return false;
    }
    return true;
  }






  /*! Comparison of two sets of points
   * The function returns true if the two containers contain the same set of points, which mean regardless to the
   * order of these elements, and the number of times these elements appear in each set.
   * @author Raffi Enficiaud
   */
  template <class container_type1, class container_type2>
  bool are_sets_of_points_equal(container_type1 c1, container_type2 c2)
  {
    // The coordinate types should be the sames
    BOOST_STATIC_ASSERT((boost::is_same<typename container_type1::value_type, typename container_type2::value_type>::value)); 

    std::sort(c1.begin(), c1.end());
    std::sort(c2.begin(), c2.end());  

    typename container_type1::iterator it1 = std::unique( c1.begin(), c1.end() );
    typename container_type2::iterator it2 = std::unique( c2.begin(), c2.end() );
  
    if(std::distance(c1.begin(), it1) != std::distance(c2.begin(), it2))
      return false;
  
    std::pair<typename container_type1::iterator, typename container_type2::iterator> p = std::mismatch(c1.begin(), it1, c2.begin());
    return p.first == it1 && p.second == it2;
  }


  //!Same as @ref are_sets_of_points_equal, but for containers being list (better sorting performances)
  template <class coordinate_type>
  bool are_sets_of_points_equal(std::list<coordinate_type> c1, std::list<coordinate_type> c2)
  {
    typedef std::list<coordinate_type> storage_compare;
    c1.sort();
    c2.sort();  

    c1.unique();
    c2.unique();
  
    if(c1.size() != c2.size())
      return false;
  
    std::pair<typename storage_compare::iterator, typename storage_compare::iterator> p = std::mismatch(c1.begin(), c1.end(), c2.begin());
    return p.first == c1.end() && p.second == c2.end();
  }


  /*! Returns true is the two sets of points are disjoint (ie. have no point in common)
   */
  template <class container_type1, class container_type2>
  bool are_sets_of_points_disjoint(container_type1 const& c1, container_type2 const& c2)
  {
    BOOST_STATIC_ASSERT((boost::is_same<typename container_type1::value_type, typename container_type2::value_type>::value)); 

    typedef std::set<typename container_type1::value_type> set1_t;
    typedef std::set<typename container_type2::value_type> set2_t;
    set1_t s1(c1.begin(), c1.end());
    set2_t s2(c2.begin(), c2.end());  

    // on peut faire aussi set_intersection dans algorithm, plus élégant mais je pense plus cher.
    // ici on a des copies des containers qu'on peut effacer à notre guise
    for(typename set1_t::iterator it(s1.begin()), ite(s1.end()); it != ite; ++it)
    {
      if(s2.count(*it) != 0)
        return false;
      #if defined(_WIN32) && defined(_MSC_VER)
      // non standard behaviour of std::set::erase under MSVC
      it = s1.erase(it);
      #else
      s1.erase(it);
      #endif
    }
    for(typename set2_t::iterator it(s2.begin()), ite(s2.end()); it != ite; ++it)
    {
      if(s1.count(*it) != 0)
        return false;
    }
    
    return true;
  }




  
  //! Returns true is the specified coordinate @ref test is inside the hyperrectangle defined by @ref rect
  template <int dim>
  bool is_point_inside(const s_hyper_rectangle<dim>& rect, const s_coordinate<dim>& test) {
    if(test[0] < rect.lowerleft_corner[0] || test[0] >= rect.upperright_corner[0])
      return false;
    for(unsigned int i = 1; i < dim; i++) {
      if(test[i] < rect.lowerleft_corner[i] || test[i] >= rect.upperright_corner[i])
        return false;
    }
    return true;
  }

  //! Specialization of @ref is_point_inside for abstract dimensional coordinates
  inline bool is_point_inside(const s_hyper_rectangle<0>& rect, const s_coordinate<0>& test) {
    YAYI_ASSERT(rect.lowerleft_corner.dimension() == test.dimension(), "Currently unsupported case for different dimensions");
    YAYI_ASSERT(rect.lowerleft_corner.dimension() != 0 && rect.upperright_corner.dimension() != 0 && test.dimension() != 0, "No dimension for one of the inputs");
      
    if(test[0] < rect.lowerleft_corner[0] || test[0] >= rect.upperright_corner[0])
      return false;
    for(unsigned int i = 1, j = test.dimension(); i < j; i++) {
      if(test[i] < rect.lowerleft_corner[i] || test[i] >= rect.upperright_corner[i])
        return false;
    }
    return true;
  }




}


#endif /* YAYI_COMMON_COORDINATES_OPERATIONS_HPP__ */
