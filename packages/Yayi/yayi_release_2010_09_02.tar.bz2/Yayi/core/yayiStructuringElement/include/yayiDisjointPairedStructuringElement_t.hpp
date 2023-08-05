/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_STRUCTURING_ELEMENT_DISJOINTPAIRED_HPP__
#define YAYI_STRUCTURING_ELEMENT_DISJOINTPAIRED_HPP__

/*!@file
 * This file defines the appropriate structure for disjoined pair of structuring element
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>
#include <Yayi/core/yayiCommon/common_coordinates_operations_t.hpp>

namespace yayi { namespace se {
  
  /*!This class mainly embbeds some logic in order to handle more easily disjoint pair of structuring element
   * It is based on a template structuring element serving as base, and provides some additionnal methods.
   * @note: this class defines a new concept for structuring elements, which is weaker than structuring elements
   * based on neighborlists. For instance, it does not implement the remove_center method.
   *
   * @author Raffi Enficiaud
   */
  template <class base_se_t>
  struct s_disjoined_paired_se : public IStructuringElement
  {
    typedef s_disjoined_paired_se<base_se_t> this_type;
    typedef typename base_se_t::element_t element_t;
  
    //! "foreground" and "background" structuring elements
    base_se_t foreground, background; 
    
    s_disjoined_paired_se(base_se_t const& fore_se, base_se_t const& back_se) : foreground(fore_se), background(back_se)
    {
      if(foreground.number_of_list() != background.number_of_list())
      {
        std::ostringstream o;
        o << "The number of lists are different for the two structuring elements (unsupported) : " 
          << "foreground : " << foreground.number_of_list() << " != (background) " << background.number_of_list();
        DEBUG_INFO(o.str());
        throw errors::yaException(o.str());
      }
    }
    
    
    //! Returns true if the underlying structuring elements have true disjoin support
    bool are_disjoint() const
    {
      for(unsigned int i = 0, j = foreground.number_of_list(); i < j; i++)
      {
        typename base_se_t::storage_type const & st1 = foreground.get_coordinates(), &st2 = background.get_coordinates();
        std::vector<typename base_se_t::coordinate_type> 
          v1(st1.begin() + i * (st1.size() / j), st1.begin() + (i + 1) * (st1.size() / j)),
          v2(st2.begin() + i * (st2.size() / j), st2.begin() + (i + 1) * (st2.size() / j));
        
        if(!are_sets_of_points_disjoint(v1, v2))
          return false;
      }
    
      return true;
    }
    
    //! Returns the transposed structuring element
    this_type transpose() const {
      return this_type(foreground.transpose(), background.transpose());
    }
    
    //! Returns the size of the structuring element
    //! Defined as being the sum of the foreground and background structuring element sizes
    unsigned int size() const {
      return foreground.size() + background.size();
    }


    /*!Returns the maximal extension of this structuring element
     * The parameter @ref dimension controls the dimension on which the extension is queried, while @ref direction 
     * specifies the direction (true for forward, false for backward). 
     */
    unsigned int maximum_extension(const unsigned int dimension, const bool direction) const {
      return std::max(foreground.maximum_extension(dimension, direction), background.maximum_extension(dimension, direction));
    }
    
    /*!Returns the maximal extension of this structuring element on every directions
     * The return value is a pair min, max, that should not be confused with the bounding box of the SE.
     */    
    std::pair<element_t, element_t> maximum_extension() const {
      std::pair<element_t, element_t> f(foreground.maximum_extension()), b(background.maximum_extension());
      
      element_t 
        min_(std::numeric_limits<typename element_t::scalar_coordinate_type>::max()), 
        max_(std::numeric_limits<typename element_t::scalar_coordinate_type>::min());
      
      for(unsigned int dimension = 0, k = foreground.get_coordinates()[0].dimension(); dimension < k; dimension++) {
        min_[dimension] = std::min(f.first[dimension], b.first[dimension]);
        max_[dimension] = std::max(f.second[dimension], b.second[dimension]);
      }
                  
      return std::make_pair(min_, max_);
    }
    
    //! Strict equality between two SE: the SE should have the same elements in the same order
    bool operator==(const this_type& r) const {
      return (this == &r) || (foreground == r.foreground && background == r.background);
    }
    bool operator!=(const this_type& r) const {
      return (this != &r) && (foreground != r.foreground || background != r.background);
    }

    /*! Test the equality against another structuring element, without taking into account the order of neighbors nor the possible
     *  duplicate elements.
     */
    bool is_equal_unordered(const this_type& r) const {
      return foreground.is_equal_unordered(r.foreground) && background.is_equal_unordered(r.background);
    }

    //IObject interface
    //! Object type
    virtual type DynamicType() const {
      return type(type::c_structuring_element, type::s_object);
    }

    //! Object description
    virtual string_type Description() const {
      static const string_type s = "Paired structuring element (foreground/background)";
      return s;
    }
    
    virtual e_structuring_element_type GetType() const {
      return e_set_paired;
    }
    virtual e_structuring_element_subtype GetSubType() const {
      return foreground.GetSubType();
    }
    
  protected:    
    virtual bool is_equal(const IStructuringElement* se) const throw() 
    {
      const this_type *se_t = dynamic_cast<const this_type *>(se);
      return (this == se_t) || ((se_t != 0) && (*this == *se_t));
    }
    
    virtual bool is_equal_unordered(const IStructuringElement* se) const throw() 
    {
      const this_type *se_t = dynamic_cast<const this_type *>(se);
      return (this == se_t) || ((se_t != 0) && this->is_equal_unordered(*se_t));
    }
    
    virtual IStructuringElement* Clone() const {
      return new this_type(*this);
    }        
    
    virtual IStructuringElement* Transpose() const
    {
      return new this_type(transpose());
    }
    virtual IStructuringElement* RemoveCenter() const
    {
      throw errors::yaException(yaRC_E_not_implemented);
    }
    virtual unsigned int GetSize() const
    {
      return size();
    }

    
  };


}} // namespace yayi::se

#endif /* YAYI_STRUCTURING_ELEMENT_DISJOINTPAIRED_HPP__ */
