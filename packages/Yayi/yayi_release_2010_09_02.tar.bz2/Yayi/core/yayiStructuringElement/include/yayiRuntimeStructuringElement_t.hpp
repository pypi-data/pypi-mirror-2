/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_RUNTIME_STRUCTURING_ELEMENT_HPP__
#define YAYI_RUNTIME_STRUCTURING_ELEMENT_HPP__

/*!@file
 * This file defines structuring elements that can be set programatically at run time
 *
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>


#include <functional>
#include <list>

namespace yayi { namespace se {

  
  namespace structuring_element {
    struct neighborhood_point_list_tag {};      //!< Tag for SE using a point list as initialization

    namespace se_tags {
      struct neighborlist_single_list   {};     //!< Tag indicating that the neighborlist has a unique list of coordinates (independant from the centers position)
      struct neighborlist_multiple_list {};     //!< Tag indicating that the neighborlist has multiple list of coordinates that depends on the center position
      
      struct structuring_element_no_reshape {};                 //!< Tag indicating that the SE does not never change its morphology
      struct structuring_element_reshape_on_coordinate {};      //!< Tag indicating that the SE does change its morphology when centered at a new coordinate
      struct structuring_element_reshape_on_coordinate_no_x {}; //!< Same as @ref structuring_element_reshape_on_coordinate, but does not change when only the first coordinate change
    }

    /*!List chooser concept
     * The list chooser concept should return the bounds of the current list on which the neighborhood iterates
     * It takes a coordinate, and returns the current list bounds.
     * @author Raffi Enficiaud
     */
    template <class coordinate_type>
    struct s_empty_behaviour : public std::unary_function<coordinate_type, yaUINT8 > 
    {
      //typedef std::unary_function<coordinate_type, std::pair<yaUINT8, yaUINT8> > parent_type;
      typedef std::unary_function<coordinate_type, yaUINT8> parent_type;
      typedef typename parent_type::result_type result_type; // Raffi : this is redundant ... but GCC signals an error I do not understand...
      
      result_type operator()(const coordinate_type&) const throw() {
        throw errors::yaException(yaRC_E_not_implemented);
        //return result_type(0);
      }
      
      template <class container>
      void init_indexes(container& c) const {
      }
    };

  }
  
  
  /*! Expose the concept of single list of coordinate for defining a structuring element
   *
   */
  template <
    class coordinate_type, 
    class se_tag_ = structuring_element::se_tags::structuring_element_no_reshape
    >
  struct neighborlist_helper_single_list {
    typedef neighborlist_helper_single_list<coordinate_type>                          this_type;
    typedef structuring_element::se_tags::neighborlist_single_list                    list_tag;
    typedef se_tag_                                                                   se_tag;
    typedef structuring_element::s_empty_behaviour<coordinate_type>                   list_chooser_t;
    
  protected:
    neighborlist_helper_single_list(bool , unsigned int) {}
    void transpose() {}
        
  public:
    neighborlist_helper_single_list(){}
    
    unsigned int number_of_list() const     {return 1;}
    //unsigned int& number_of_list()          {return throw errors::yaException(yaRC_E_not_implemented);}    
    bool has_multiple_list() const          {return false;}

    list_chooser_t get_list_chooser() const throw() {return list_chooser_t();}  
  };
  


  /*! Expose the concept of multiple lists of coordinate for defining a structuring element (the structuring element
   *  can reshape itself according to the center point).
   *
   */
  template <
    class coordinate_type,
    class list_chooser_t_ = structuring_element::s_empty_behaviour<coordinate_type>,
    class se_tag_ = structuring_element::se_tags::structuring_element_reshape_on_coordinate
    >
  struct neighborlist_helper_multiple_list {
    
    typedef neighborlist_helper_multiple_list<coordinate_type, list_chooser_t_, se_tag_>  this_type;

    typedef structuring_element::se_tags::neighborlist_multiple_list         list_tag;  // this behaviour
    typedef se_tag_                                                          se_tag;
    typedef list_chooser_t_                                                  list_chooser_t;

  public:
    neighborlist_helper_multiple_list() : m_b_transposed(false), m_number_of_lists(1) {}
    neighborlist_helper_multiple_list(bool transposed, unsigned int nb_list) : m_b_transposed(transposed), m_number_of_lists(nb_list) {
    }   
    
    bool has_multiple_list() const          {return number_of_list() > 1;}
    unsigned int number_of_list() const     {return m_number_of_lists;}
    unsigned int& number_of_list()          {return m_number_of_lists;}
    list_chooser_t get_list_chooser() const throw() {
      return list_chooser_t(m_b_transposed);
    }
    
  protected:
    void transpose() { m_b_transposed = !m_b_transposed; }

    bool m_b_transposed;
    unsigned int m_number_of_lists;
  
  };
  
  

  /*! A simple structuring element coding the shifts around the center (0) as image coordinates
   *
   * @author Raffi Enficiaud
   */
  template <
    class coordinate_type_, 
    class element_t_ = coordinate_type_,    
    class se_specific_ = neighborlist_helper_single_list<coordinate_type_>
    >
  struct s_neighborlist_se : 
    public IStructuringElement, 
    public se_specific_
  {
  private:
    typedef se_specific_ helper_t;
    typedef s_neighborlist_se<coordinate_type_, element_t_, se_specific_> this_type;
  
  public:
    typedef element_t_                            element_t;
    typedef std::vector<element_t>                storage_type;
    typedef coordinate_type_                      coordinate_type;
    typedef typename storage_type::iterator       iterator;
    typedef typename storage_type::const_iterator const_iterator;

    typedef typename helper_t::se_tag             se_tag;
  
  protected:
    s_neighborlist_se(const se_specific_& r_se, const storage_type& v = storage_type()) : se_specific_(r_se), vector_coordinate(v)
    {}
    
  public:
    
    
    //! Default constructor
    s_neighborlist_se() : se_specific_(), vector_coordinate()
    {}
    
    
    //! Constructor taking as argument a vector for each point of the structuring element and an argument
    //! indicating the number of lists (defauting to 1)
    s_neighborlist_se(const storage_type& v) : 
      se_specific_(),
      vector_coordinate(v)
    {}
    

    s_neighborlist_se(const std::vector<typename storage_type::value_type::scalar_coordinate_type>& v) : 
      se_specific_(),
      vector_coordinate(coordinate_type::from_table_multiple(v.begin(), v.end())) 
    {}
    
    const_iterator begin() const {
      return vector_coordinate.begin();
    }

    const_iterator end() const {
      return vector_coordinate.end();
    }
    
    yaRC set_coordinates(const storage_type& v) {
      vector_coordinate = v;
      return yaRC_ok;
    }
    
    const storage_type& get_coordinates() const throw() {
      return vector_coordinate;
    }
    
    //! Returns a transposed copy of this structuring element
    //! TODO capitaliser dans une structure helper
    this_type transpose() const {
      this_type ret(static_cast<const se_specific_&>(*this), transpose_set(vector_coordinate));
      ret.se_specific_::transpose();
      return ret;
    }

    //! Returns a copy of this structuring element without the center
    //! TODO capitaliser dans une structure helper
    this_type remove_center() const {
      static const element_t center = element_t(0);
      storage_type out;
      for(typename storage_type::const_iterator it(vector_coordinate.begin()), ite(vector_coordinate.end());
          it != ite;
          ++it) 
      {
        if(*it == center) continue;
        out.push_back(*it);
      }
      return this_type(static_cast<const se_specific_&>(*this), out);
    }
    
    //! Returns the size of the structuring element
    unsigned int size() const {
      return static_cast<unsigned int>(vector_coordinate.size());    
    }
    
    /*!Returns the maximal extension of this structuring element
     * The parameter @ref dimension controls the dimension on which the extension is queried, while @ref direction 
     * specifies the direction (true for forward, false for backward). 
     */
    unsigned int maximum_extension(const unsigned int dimension, const bool direction) const {
      if(direction) {
        typename element_t::scalar_coordinate_type extension = 0;
        for(unsigned int i = 0; i < vector_coordinate.size(); i++) {
          extension = std::max(extension, vector_coordinate[i][dimension]);
        }
        return extension;
      }
      else {
        typename element_t::scalar_coordinate_type extension = 0;
        for(unsigned int i = 0; i < vector_coordinate.size(); i++) {
          extension = std::max(extension, -vector_coordinate[i][dimension]);
        }
        return extension;
      }
    }


    /*!Returns the maximal extension of this structuring element on every directions
     * The return value is a pair min, max, that should not be confused with the bounding box of the SE.
     */    
    std::pair<element_t, element_t> maximum_extension() const {
      element_t 
        min_(std::numeric_limits<typename element_t::scalar_coordinate_type>::max()), 
        max_(std::numeric_limits<typename element_t::scalar_coordinate_type>::min());
      
      for(unsigned int i = 0, j = vector_coordinate.size(); i < j; i++) {
        for(unsigned int dimension = 0, k = vector_coordinate[i].dimension(); dimension < k; dimension++) {
          min_[dimension] = std::min(min_[dimension], vector_coordinate[i][dimension]);
          max_[dimension] = std::max(max_[dimension], vector_coordinate[i][dimension]);
        }
      }
      
      return std::make_pair(min_, max_);
    }
    
    
    //! Strict equality between two SE: the SE should have the same elements in the same order
    bool operator==(const this_type& r) const {
      return (this == &r) || (vector_coordinate == r.vector_coordinate);
    }
    bool operator!=(const this_type& r) const {
      return (this != &r) && (vector_coordinate != r.vector_coordinate);
    }
    
    
    /*! Test the equality against another structuring element, without taking into account the order of neighbors nor the possible
     *  duplicate elements.
     */
    bool is_equal_unordered(const this_type& r) const {
      return are_sets_of_points_equal(vector_coordinate, r.vector_coordinate);
    }
    
    //!@group Virtual methods inherited from IObject
    //!@{
    //! Object type
    virtual type DynamicType() const {
      return type(type::c_structuring_element, type::s_object);
    }

    //! Object description
    virtual string_type Description() const {
      static const string_type s = "Generic structuring element built on neighbor lists";
      return s;
    }
    //!@}
    
    //!@group Virtual methods inherited from IStructuringElement
    //!@{
    virtual structuring_element_type GetType() const {
      return e_set_neighborlist;
    }
    
    virtual e_structuring_element_subtype GetSubType() const {
      return e_sest_neighborlist_generic_single;
    }
    
  protected:
    virtual unsigned int GetSize() const {
      return size();
    }
    
    virtual IStructuringElement* Transpose() const {
      return new this_type(this->transpose());
    }
    
    virtual IStructuringElement* RemoveCenter() const {
      return new this_type(this->remove_center());
    }

    virtual IStructuringElement* Clone() const {
      return new this_type(*this);
    }
    
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
    
    //!@}
    
  protected:
    storage_type vector_coordinate;
    helper_t helper;
  };
  
  
}}
  
  

#endif /* YAYI_RUNTIME_STRUCTURING_ELEMENT_HPP__ */
