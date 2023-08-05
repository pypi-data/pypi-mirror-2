/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_HISTOGRAM__HPP___
#define YAYI_COMMON_HISTOGRAM__HPP___

/*! @file
 *  @brief Histogram generic definition and manipulation
 */


#include <map>
#include <functional>
#include <vector>
#include <algorithm>
#include <numeric>

#include <Yayi/core/yayiCommon/include/common_types_T.hpp>




namespace yayi
{
  /*! @brief Generic histogram structure
   *
   * @author Raffi Enficiaud
   */
  template <typename bin_t = yaF_double, typename count_t = yaUINT32>
  struct s_histogram_t : public std::map<bin_t, count_t>
  {

  public:
    typedef bin_t      bin_type;         //! Representation type of the bins
    typedef count_t    count_type;       //! Representation type of the counted elements
    typedef std::map<bin_t, count_t> representation_type;

    s_histogram_t() : representation_type() {}
    
    //! Returns the maximum non-zero bin
    bin_type max_bin() const throw(){return this->max_element();}

    //! Returns the minimum non-zero bin
    bin_type min_bin() const throw(){return this->min_element();}

    //! Returns the sum of the bins
    typename type_description::s_sum_supertype<count_type>::type sum() const
    {
      typedef std::plus<typename s_sum_supertype<count_type>::type> op_type;
      return std::accumulate(this->begin(), this->end(), 0, op_type());
    }
    
    //! Clears the content of the histogram
    void clear()
    {
      this->clear();
    }
    
    //! Normalizes the histogram in regards to its sum (returns a new histogram)
    s_histogram_t<bin_type, yaF_double> normalise() const
    {
      s_histogram_t<bin_type, yaF_double> out;
      typename type_description::s_sum_supertype<count_type>::type const sum_ = sum();
      
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end());
          it != ite;
          ++it)
      {
        out[it->first] = it->second / sum_;
      }
      return out;
      
    }
  };


  /*! @brief Generic histogram structure (specialization for 8bits unsigned type)
   *
   * @author Raffi Enficiaud
   */
  template <typename count_t>
  struct s_histogram_t<yaUINT8, count_t> : public std::vector<count_t>
  {
  public:
    typedef yaUINT8    bin_type;         //! Representation type of the bins
    typedef count_t    count_type;       //! Representation type of the counted elements
    typedef std::vector<count_t> representation_type;

    s_histogram_t() : representation_type(std::numeric_limits<bin_type>::max(), count_t(0)) 
    {}
    
    //! Returns the maximum non-zero bin
    bin_type max_bin() const throw()
    {
      bin_type bin = std::numeric_limits<yaUINT8>::max();
      for(typename representation_type::const_reverse_iterator it(this->rbegin()), ite(this->rend()); 
          it != ite;
          ++it, --bin)
      {
        if(*it)
          return bin;
      }
      return std::numeric_limits<yaUINT8>::max();
    }
    
    //! Returns the minmum non-zero bin
    bin_type min_bin() const throw(){
      bin_type bin = std::numeric_limits<yaUINT8>::min();
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end()); 
          it != ite;
          ++it, ++bin)
      {
        if(*it)
          return bin;
      }
      return std::numeric_limits<yaUINT8>::min();
    }

    //! Returns the total sum of the histogram
    typename type_description::s_sum_supertype<count_type>::type sum() const
    {
      typedef std::plus<typename s_sum_supertype<count_type>::type> op_type;
      return std::accumulate(this->begin(), this->end(), 0, op_type());
    }
    
    //! Clears the content of the histogram
    void clear()
    {
      for(typename representation_type::iterator it(this->begin()), ite(this->end()); it != ite; ++it)
      {
        *it = 0;
      }    
    }
    
    //! Normalizes the histogram with its sum (returns a new histogram with yaF_double type count)
    s_histogram_t<bin_type, yaF_double> normalise() const
    {
      s_histogram_t<bin_type, yaF_double> out;
      typename type_description::s_sum_supertype<count_type>::type const sum_ = sum();
      
      for(typename representation_type::const_iterator it(this->begin()), ite(this->end());
          it != ite;
          ++it)
      {
        out[it->first] = it->second / sum_;
      }
      return out;
      
    }
  };

} // namespace yayi

#endif /* YAYI_COMMON_HISTOGRAM__HPP___ */
