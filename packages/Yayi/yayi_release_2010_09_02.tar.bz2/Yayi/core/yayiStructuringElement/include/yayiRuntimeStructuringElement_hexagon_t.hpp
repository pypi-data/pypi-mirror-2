/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_RUNTIME_STRUCTURING_ELEMENT_HEXAGON_HPP__
#define YAYI_RUNTIME_STRUCTURING_ELEMENT_HEXAGON_HPP__

/*!@file
 * This file defines the hexagonal structuring element. More precisely, it instanciates 
 * the correct list chooser (alternating on the y axis). 
 */

#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>

namespace yayi { namespace se {


  /*! This helper class implements the centering behaviour concept for hexagonal structuring element
   *  It basically returns two alternating neighbor list along y axis. 
   */
  template <class coordinate_type>
  struct s_alternating_on_y_behaviour : public std::unary_function<coordinate_type, yaUINT8 > 
  {
    typedef std::unary_function<coordinate_type, yaUINT8> parent_type;
    typedef typename parent_type::result_type result_type; // Raffi : this is redundant ...
    
    s_alternating_on_y_behaviour(bool is_transposed_) : 
      //min_(std::numeric_limits<unsigned int>::max()), med_(min_), max_(min_),
      is_transposed(is_transposed_)
    {} 
    
    result_type operator()(const coordinate_type& p) const throw() {
      //return [min_, med_[, or [med_, max_[
      return ((static_cast<yaUINT8>(p[1]) & 1) == 0) ^ is_transposed;
    }

    result_type operator()(const offset o) const throw() {
      //return [min_, med_[, or [med_, max_[
      return ((static_cast<yaUINT8>(o / off_x) & 1) == 0) ^ is_transposed;
    }
    
    template <class se_t, class im_t, class container>
    void init_indexes(const se_t& se, const im_t& im_, container& c) {
      DEBUG_ASSERT(se.size() % 2 == 0, "The number of points is odd (incorrect)");
      c.clear();
      c.push_back(std::make_pair(0, se.size() / 2));
      c.push_back(std::make_pair(se.size() / 2, se.size()));
      off_x = im_.Size()[0];
    }
    const bool  is_transposed;
    offset      off_x;
  };


  /*! Implements the behaviour of an hexagon structuring element.
   *  This SE does not reshape on x shifts, but does reshape on all other type of shifts.
   *  It contains two alternating lists of structuring elements.
   */
  template <
    class coordinate_type,
    class element_t = coordinate_type,    
    class se_specific_ = neighborlist_helper_multiple_list<
                          coordinate_type,
                          s_alternating_on_y_behaviour<coordinate_type>,
                          structuring_element::se_tags::structuring_element_reshape_on_coordinate_no_x>
    >
  struct s_neighborlist_se_hexa_x : 
    public s_neighborlist_se <coordinate_type, element_t, se_specific_>
  {
  public:
    typedef s_neighborlist_se<coordinate_type, element_t, se_specific_> parent_type;
    typedef typename parent_type::storage_type storage_type;
    typedef s_neighborlist_se_hexa_x<coordinate_type, element_t, se_specific_> this_type;
  
    s_neighborlist_se_hexa_x() : parent_type(se_specific_(false, 2)) {}
       
    s_neighborlist_se_hexa_x(const storage_type& v) : parent_type(se_specific_(false, 2), v) {}
    
    s_neighborlist_se_hexa_x(const std::vector<typename storage_type::value_type::scalar_coordinate_type>& v) : 
      parent_type(se_specific_(false, 2), coordinate_type::from_table_multiple(v.begin(), v.end())) 
    {}
    
    virtual e_structuring_element_subtype GetSubType() const {
      return e_sest_neighborlist_hexa;
    }
    
    //! Returns a copy of this structuring element without the center
    this_type remove_center() const {
      static const element_t center = element_t(0);
      storage_type out;
      for(typename storage_type::const_iterator it(this->vector_coordinate.begin()), ite(this->vector_coordinate.end());
          it != ite;
          ++it) 
      {
        if(*it == center) continue;
        out.push_back(*it);
      }
      
      // this is for initializing all of the states of the structuring element
      this_type ret(*this);
      ret.set_coordinates(out);
      return ret;
    }
    
     this_type transpose() const {
      typedef typename parent_type::storage_type storage_type;
      if(are_sets_of_points_equal(
          storage_type(this->vector_coordinate.begin(), this->vector_coordinate.begin() + this->vector_coordinate.size() / 2),
          transpose_set(storage_type(this->vector_coordinate.begin() + this->vector_coordinate.size() / 2, this->vector_coordinate.end()))
          )
        )
      {
        this_type ret(*this);
        ret.se_specific_::transpose();
        return ret;
      }

      this_type ret(*this);
      transpose_set_in_place(ret.vector_coordinate);
      ret.se_specific_::transpose();
      return ret;
    }
    
    bool operator==(const this_type& r) const {
      return this->m_b_transposed == r.m_b_transposed && this->parent_type::operator==(r);
    }
    bool operator!=(const this_type& r) const {
      return this->m_b_transposed != r.m_b_transposed || this->parent_type::operator!=(r);
    }


    /* Returns true if each "sub" structuring element (each list of coordinates for a given center) contains the same elements.
     * The comparison takes into account the transposition information of the structuring element, which means that if the SE do
     * not have the same transposition flag, first list of current SE is compared to second list of argument SE, and vice versa.
     */
    bool is_equal_unordered(const this_type& r) const {
    
      typedef typename parent_type::storage_type storage_type;
      
      // yeah I know these lines are badly written, but it is to avoid useless copies of containers
      return 
        are_sets_of_points_equal(
          storage_type(this->vector_coordinate.begin(), this->vector_coordinate.begin() + this->vector_coordinate.size() / 2),
          (this->m_b_transposed == r.m_b_transposed ? 
            storage_type(r.vector_coordinate.begin(), r.vector_coordinate.begin() + r.vector_coordinate.size() / 2) : 
            storage_type(r.vector_coordinate.begin() + r.vector_coordinate.size() / 2, r.vector_coordinate.end())
          )
        )
        
        && 
        
        are_sets_of_points_equal(
          storage_type(this->vector_coordinate.begin() + this->vector_coordinate.size() / 2, this->vector_coordinate.end()),
          (this->m_b_transposed != r.m_b_transposed ? 
            storage_type(r.vector_coordinate.begin(), r.vector_coordinate.begin() + r.vector_coordinate.size() / 2) : 
            storage_type(r.vector_coordinate.begin() + r.vector_coordinate.size() / 2, r.vector_coordinate.end())
          )
        );
    }    

    
    //IObject interface
    //! Object type
    virtual type DynamicType() const {
      return type(type::c_structuring_element, type::s_object);
    }

    //! Object description
    virtual string_type Description() const {
      static const string_type s = "Structuring element reshaping along Y";
      return s;
    }
    
  protected:    
    virtual bool is_equal(const IStructuringElement* se) const throw() 
    {
      const this_type *se_t = dynamic_cast<const this_type *>(se);
      return (se_t != 0) && (*this == *se_t);
    }
    
    virtual bool is_equal_unordered(const IStructuringElement* se) const throw() 
    {
      const this_type *se_t = dynamic_cast<const this_type *>(se);
      return (se_t != 0) && this->is_equal_unordered(*se_t);
    }
    
    virtual IStructuringElement* Clone() const {
      return new this_type(*this);
    }    


  };


} }

#endif /* YAYI_RUNTIME_STRUCTURING_ELEMENT_HEXAGON_HPP__ */
