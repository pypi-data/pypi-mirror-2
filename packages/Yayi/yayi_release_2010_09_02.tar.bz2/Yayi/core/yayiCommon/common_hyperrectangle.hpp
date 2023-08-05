/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_HYPER_RECTANGLE_HPP__
#define YAYI_COMMON_HYPER_RECTANGLE_HPP__


/*!@file
 * This file defines the hyperrectangle structure, used to define subspaces in images
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiCommon/common_coordinates.hpp>

namespace yayi
{

  /*!@brief "Hyper" Rectangle type for a given dimension
  *  @author Raffi Enficiaud
  */
  template <int dim> 
  struct s_hyper_rectangle
  {
    typedef s_hyper_rectangle<dim> this_type;
    typedef s_coordinate<dim> coordinate_type;

    coordinate_type lowerleft_corner, upperright_corner;

    //! Hyperrectangle default constructor
    s_hyper_rectangle() : lowerleft_corner(), upperright_corner()
    {}

    //! Copy constructs an hyperrectangle
    s_hyper_rectangle(const this_type& r) :
      lowerleft_corner(r.lowerleft_corner), upperright_corner(r.upperright_corner)
    {}
    
    //! Constructs an hyperrectangle from an origin and a size
    s_hyper_rectangle(const coordinate_type& lower_left, const coordinate_type& size) :
      lowerleft_corner(lower_left), upperright_corner(size + lower_left)
    {
      YAYI_ASSERT(lowerleft_corner.dimension() == upperright_corner.dimension(), "Corners of different dimension");
    }
    
    //! Returns the size spanned by the hyperrectangle
    coordinate_type Size() const throw()
    {
      return upperright_corner - lowerleft_corner;
    }

    //! Sets the size of the hyperrectangle
    void SetSize(const coordinate_type& size) throw()
    {
      upperright_corner = size + lowerleft_corner;
    }

    //! Sets the origin of the hyperrectangle, preserves the size
    void SetOrigin(const coordinate_type& origin) throw()
    {
      coordinate_type s = Size();
      lowerleft_corner = origin;
      upperright_corner = s + lowerleft_corner;
    }

    //! Returns the origin of the hyperrectangle (lowerleft corner)
    coordinate_type const& Origin() const throw()
    {
      return lowerleft_corner;
    }
    
    //! Returns true if the argument hyperrectangle has the same geometry, false otherwise
    bool operator==(const this_type& r) const throw()
    {
      return &r == this || (r.lowerleft_corner == lowerleft_corner && r.upperright_corner == upperright_corner);
    }
    
    //! Returns true if the specified point is inside the rectangle
    bool is_inside(const coordinate_type& c) const
    {
      YAYI_ASSERT(lowerleft_corner.dimension() == upperright_corner.dimension(), "Corners of different dimension");
      for(unsigned int i = 0; i < lowerleft_corner.dimension(); i++)
      {
        const typename coordinate_type::scalar_coordinate_type p = c[i];
        if(p < lowerleft_corner[i] || p >= upperright_corner[i])
          return false;
      }
      return true;
    }
  };





 
} 

#endif /* YAYI_COMMON_HYPER_RECTANGLE_HPP__ */
