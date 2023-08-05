/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_IMAGE_ALLOCATORS_T_HPP__
#define YAYI_IMAGE_ALLOCATORS_T_HPP__


/*@file
 *@brief Image allocators
 * 
 * Image allocators define the way images are represented in memory. The simplest way is a standard array without 
 * any padding  (@ref s_default_image_allocator).
 *
 *
 */


#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>

namespace yayi
{

  /*!@brief Standard allocator for pixel maps
   *
   */
  template <
    class pixel_type_t, 
    class coordinate_type_t>
  struct s_default_image_allocator
  {
    typedef pixel_type_t                                            pixel_type;
    typedef coordinate_type_t                                       coordinate_type;
    typedef s_default_image_allocator<pixel_type, coordinate_type>  this_type;

    typedef offset                                                  offset_type;
    typedef offset                                                  typed_offset_type;

    typedef pixel_type*																							pixel_map_type;

    coordinate_type	size;
    
    //! Checks the validity of the input coordinate in terms of allocating
    bool checkCoordinate(const coordinate_type& coord) const throw() {
      for(unsigned int i = 0; i < coord.dimension(); i++) {
        if(coord[i] <= 0) {
          return false;
        }
      }
      return true;
    }

    //! Allocates the pixel map
    pixel_map_type allocate(const coordinate_type& coord)
    {
      if(!checkCoordinate(coord))
        return 0;

      return new (std::nothrow) pixel_type[total_number_of_points(coord)];			// pour l'instant, il s'agit d'une allocation C++ simple. On pourra envisager des classes avec du padding par la suite
    }

    //! Frees the pixel map
    pixel_map_type& deallocate(pixel_map_type& pix_map)
    {
      if(pix_map == 0)
        return pix_map;
      delete [] pix_map;
      pix_map = 0;
      //size.clear();
      return pix_map;
    }

    //! Transforms a coordinate 
    offset_type from_coordinate_to_offset(const coordinate_type& coord) const
    {
      DEBUG_ASSERT(size.dimension() != 0, "Uninitialized size");
      return yayi::from_coordinate_to_offset(size, coord);
    }

    //! Transforms a coordinate to a typed offset (an offset which should be added as byte)
    typed_offset_type from_coordinate_to_typed_offset(const coordinate_type& coord) const
    {
      return from_coordinate_to_offset(coord) * sizeof(pixel_type);
    }
  };


  //! Utility template structure for transforming the type of the pixel into another for an allocator object (hence retaining the other parameters)
  template <class pixel_t, class allocator_t>
  struct s_get_same_allocator_of_t
  {
  };

  template <class pixel_t, class pixel_init_t, class coordinate_type_t>
  struct s_get_same_allocator_of_t< pixel_t, s_default_image_allocator<pixel_init_t, coordinate_type_t> >
  {
    typedef s_default_image_allocator<pixel_t, coordinate_type_t> type;
  };



} // namespace yayi


#endif

