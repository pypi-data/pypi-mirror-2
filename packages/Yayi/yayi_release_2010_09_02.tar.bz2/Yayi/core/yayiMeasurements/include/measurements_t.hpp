/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_MEASUREMENTS_T_HPP__
#define YAYI_MEASUREMENTS_T_HPP__

#include <vector>
#include <map>
#include <functional>


namespace yayi
{
  namespace measurements
  {

    template <class image_pixel_t, class region_index_t, class op_region_t>
    struct s_measurement_on_regions: public std::binary_function<image_pixel_t, region_index_t, void>
    {
      typedef std::map<region_index_t, op_region_t> map_meas_t;
      map_meas_t map_;
      typedef std::map<region_index_t, typename op_region_t::result_type> result_type;
      s_measurement_on_regions() : map_() {}
      void operator()(const image_pixel_t& p, const region_index_t& r) throw()
      {
        map_[r](p);
      }
      
      result_type result() const
      {
        result_type out;
        for(typename map_meas_t::const_iterator it(map_.begin()), ite(map_.end()); 
            it != ite;
            ++it)
        {
          out[it->first] = it->second.result();
        }
        return out;
      }
      
      
    };


    template <class image_pixel_t, class mask_t, class op_region_t>
    struct s_measurement_on_mask: public std::binary_function<image_pixel_t, mask_t, void>
    {
      op_region_t op_;
      const mask_t value_;
      s_measurement_on_mask() : op_(), value_() {}
      s_measurement_on_mask(const mask_t & value) : op_(), value_(value) {}
      void operator()(const image_pixel_t& p, const mask_t& r) throw()
      {
        if(r == value_) 
          op_(p);
      }
      
    };



  }
}



#endif /* YAYI_MEASUREMENTS_T_HPP__ */
