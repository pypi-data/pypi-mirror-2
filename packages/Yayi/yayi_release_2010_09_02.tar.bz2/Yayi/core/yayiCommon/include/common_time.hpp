/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_TIME_HPP__
#define YAYI_COMMON_TIME_HPP__

/*!@file
 * This file contains functions relative to time measurements (mainly for benchmarking purposes)
 *
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

namespace yayi
{
  namespace time
  {
  
    /*!@brief Utility class for time elapse measurements
     * This class merely wraps some known functions in boost::posix_time
     * @author Raffi Enficiaud
     */
    struct s_time_elapsed
    {
      boost::posix_time::ptime time;
      
      s_time_elapsed() : time(boost::posix_time::microsec_clock::local_time()) {}
      s_time_elapsed(const s_time_elapsed& r_) : time(r_.time) {}
      
      double total_microseconds() const 
      {
        //int count = number_of_tenths*(time_duration::ticks_per_second()/10);

        return static_cast<double>((boost::posix_time::microsec_clock::local_time() - time).total_microseconds());
        //return ((boost::posix_time::microsec_clock::local_time() - time).ticks() / boost::posix_time::time_duration::ticks_per_second());
      }

      double total_milliseconds() const 
      {
        //int count = number_of_tenths*(time_duration::ticks_per_second()/10);

        return static_cast<double>((boost::posix_time::microsec_clock::local_time() - time).total_milliseconds());
        //return ((boost::posix_time::microsec_clock::local_time() - time).ticks() / boost::posix_time::time_duration::ticks_per_second());
      }
      

    };
  
    //! Returns the string representation of the current date and time.
    string_type current_date_and_time_as_string()
    {
      return boost::posix_time::to_simple_string(boost::posix_time::microsec_clock::local_time());
    }  
  }
}

#endif /* YAYI_COMMON_TIME_HPP__ */
