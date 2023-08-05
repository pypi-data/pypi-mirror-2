/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_RUNTIME_NEIGHBORHOOD_HPP__
#define YAYI_RUNTIME_NEIGHBORHOOD_HPP__

/*!@file
 * This file defines neighborhoods that can be set programatically at run time
 *
 * @author Raffi Enficiaud
 */
 
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
 
#include <boost/tuple/tuple.hpp>

namespace yayi { namespace se {

  template <class element_it_t, class image_t> struct s_offset_list_iterator_const;
  template <class element_it_t, class image_t> struct s_offset_list_iterator;
  
  
  /*! Iterator of the neighborhood
   *
   */
  template <
    class element_it_t, 
    class image_t
  >
  struct s_offset_list_iterator_const : public IConstIterator
  {
    typedef IConstIterator parent_type;
    typedef IConstIterator interface_type;
    typedef s_offset_list_iterator_const<element_it_t, image_t> this_type;
    
    // Concept check : element_it_t should be a random access iterator
    
    //typedef typename element_it_t::value_type value_type;
    typedef typename image_t::pixel_type value_type;
    typedef typename image_t::coordinate_type coordinate_type;
    typedef typename parent_type::pixel_type interface_pixel_type;
    typedef typename parent_type::coordinate_type interface_coordinate_type;
    
    typedef typename image_t::const_reference const_reference;
    typedef typename element_it_t::value_type offset_type;
  
    typedef std::random_access_iterator_tag         iterator_category;
    typedef typename element_it_t::difference_type  difference_type;
    typedef value_type*                             pointer;
    typedef const_reference                         reference;


    s_offset_list_iterator_const(
      image_t&im_, 
      element_it_t const& it_
      ): it(it_), im(&im_) {}
    
    s_offset_list_iterator_const(const this_type& it_): it(it_.it), im(it_.im) {}
    s_offset_list_iterator_const(const s_offset_list_iterator<element_it_t, typename remove_const<image_t>::type>& it_) : it(it_.it), im(it_.im) {}

    
    //! Deference operator
    const_reference operator*() const {
      return im->pixel(*it);
    }
    
    //! Distance operator
    difference_type operator-(const this_type& r_) const {
      return it - r_.it;
    }

    //! Less than comparable
    bool operator<(const this_type& r_) const {
      return it < r_.it;
    }

    //! Random access non mutable
    const_reference operator[](const difference_type n) const {
      return *(it + n);
    }

    //! Addition
    this_type& operator+=(const difference_type n) {
      it += n;
      return *this;
    }
    
    //! Addition
    this_type operator+(const difference_type n) const {
      this_type ret(*this);
      ret.it += n;
      return ret;
    }
    //! Addition (external)
    friend this_type operator+(const difference_type n, const this_type& r) 
    {
      this_type ret(r);
      ret += n;
      return ret;
    }

    //! Subtraction
    this_type& operator-=(const difference_type n) {
      it -= n;
      return *this;
    }

    //! Subtraction
    this_type operator-(const difference_type n) const {
      this_type ret(*this);
      ret -= n;
      return ret;
    }
    //! Subtraction (external)
    friend this_type operator-(const difference_type n, const this_type& r) 
    {
      this_type ret(r);
      ret -= n;
      return ret;
    }



    //! Increment operator (only for non end iterators)
    this_type& operator++() {
      ++it;
      return *this;
    }

    //! Decrement operator (only for non end iterators)
    this_type& operator--() {
      --it;
      return *this;
    }
    
    // Additional iterator semantics
    offset_type Offset() const {
      return *it;
    }
    
    coordinate_type Position() const {
      return from_offset_to_coordinate(im->Size(), *it);
    }
    
    bool operator==(this_type const& it_r) const {return it == it_r.it;}
    bool operator!=(this_type const& it_r) const {return it != it_r.it;}

    
  protected:  
    //!@group IConstIterator interface @{
    virtual bool is_equal(const interface_type* const& it_interface) const {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("Unable to compare iterators of different kind");
      return (*this) == (*it_);    
    }

    virtual bool is_different(const interface_type* const& it_interface) const {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("Unable to compare iterators of different kind");
      return (*this) != (*it_);    
    }
    
    virtual interface_coordinate_type GetPosition() const throw() {
      return interface_coordinate_type(Position());
    }

    virtual yaRC SetPosition(const interface_coordinate_type&) throw() {
      return yaRC_E_not_implemented;
    }
    
    virtual offset GetOffset() const throw() {
      return Offset();
    }    
    
    virtual yaRC next() {
      this->operator++();
      return yaRC_ok;
    }
    
    virtual yaRC previous() {
      this->operator--();
      return yaRC_ok;
    }
    
    virtual interface_pixel_type getPixel() const {
      return interface_pixel_type(*(*this));
    }
    virtual this_type* clone() const throw() {
      // this works because the children classes do not have special copy constructors ?
      return new this_type(*this);
    }    
    //!@}
    
    
    //!@group IObject interface @{
    virtual type DynamicType () const
    {
      //@todo proper type setting
      static const type t(type::c_iterator, type::s_image); // TODO ajouter un type ici
      return t;
    }

    virtual string_type Description() const
    {
      return "Neighborhood offset list iterator";
    }    
    //!@}
    
  protected:
    element_it_t it;
    image_t * im;
  };
  
  
  
  template <
    class element_it_t, 
    class image_t
  >
  struct s_offset_list_iterator : 
    public s_offset_list_iterator_const<element_it_t, image_t>, 
    public IIterator
  {
  
    typedef s_offset_list_iterator_const<element_it_t, image_t> parent_type;
    
    s_offset_list_iterator(
      image_t&im_, 
      element_it_t const& it_
      ): parent_type(im_, it_) 
    {}
    
    s_offset_list_iterator(
      const parent_type& it_): parent_type(it_) 
    {}

    typedef typename image_t::reference reference;
    //! Deference operator
    reference operator*() {
      return parent_type::im->pixel(*parent_type::it);
    }

    //! Random access mutable
    reference operator[](const typename parent_type::difference_type n) {
      return *(parent_type::it + n);
    }

    friend struct s_offset_list_iterator_const<element_it_t, typename boost::add_const<image_t>::type>;
    
    
  protected:
    virtual yaRC setPixel(const typename parent_type::interface_pixel_type& p) {
      *(*this) = p.operator typename parent_type::value_type();
      return yaRC_ok;
    }    
  };
  
  
  
  
  
  
  //! This is a facade for s_runtime_neighborhood
  template <class list_chooser_tag, class image_t, class se_t>
  struct s_runtime_neighborhood_helper;
  
  /*!Facade for special structuring elements that do not reshape by a change of center
   *
   * @author Raffi Enficiaud
   */
  template <class image_t, class se_t>
  struct s_runtime_neighborhood_helper<structuring_element::se_tags::structuring_element_no_reshape, image_t, se_t> {
  
    s_runtime_neighborhood_helper(const image_t&, const se_t& se) : begin_index(0), end_index(se.size()) {}
    
    void center(typename image_t::coordinate_type const & ) const throw() {
      // The shape of SE does not change: nothing to do here
    }

    void center(typename image_t::offset_type ) const throw() {
      // The shape of SE does not change: nothing to do here
    }
    
    void set_shift(typename image_t::coordinate_type const & ) const throw() {
      // All is performed in the neighborhood, nothing to be done here
    }

    void set_shift(typename image_t::offset_type ) const throw() {
      // All is performed in the neighborhood, nothing to be done here
    }
    
    void shift_center() const throw() {
      // All is performed in the neighborhood, nothing to be done here
    }
    
    void compute_shifted() {
      // This SE does not reshape itself, no other shape is considered
    } 
    
    typedef unsigned int index_t;
    // The SE does not reshape: these indexes are const
    const index_t begin_index, end_index;

  
  };
  
  
  /*!Facade for special structuring elements that do reshape on all coordinates except along the x axis
   *
   * @author Raffi Enficiaud
   */
  template <class image_t, class se_t>
  struct s_runtime_neighborhood_helper<structuring_element::se_tags::structuring_element_reshape_on_coordinate_no_x, image_t, se_t> {
    typename se_t::list_chooser_t ob_chooser;
  
    s_runtime_neighborhood_helper(const image_t& im_, const se_t& se) : 
      ob_chooser(se.get_list_chooser()), begin_index(0), end_index(se.size())
      #ifndef NDEBUG
      , im(im_)
      #endif
    {
      ob_chooser.init_indexes(se, im_, vect_indexes);
    }
    
    
    //! Centers the SE
    //! Full centering of the structuring element
    void center(typename image_t::coordinate_type const & c) throw() {
      boost::tie(begin_index, end_index) = vect_indexes[ob_chooser(c)];
    }

    void center(typename image_t::offset_type o) throw() {
      boost::tie(begin_index, end_index) = vect_indexes[ob_chooser(o)];
    }

    void set_shift(typename image_t::coordinate_type const & c) YAYI_THROW_DEBUG_ONLY__ {
      #ifndef NDEBUG
      DEBUG_ASSERT(c[0] > 0, "No shift on X ?");
      for(int i = 1; i < c.dimension(); i++) {
        DEBUG_ASSERT(c[i] == 0, "This SE does not support any shift on dimension on other than x");
      }
      #endif
    }

    void set_shift(typename image_t::offset_type o) YAYI_THROW_DEBUG_ONLY__ {
      DEBUG_ASSERT(o >= 1 && o < im.Size()[0], "This SE does not support any shift on dimension other than x (or check that images are organised in scan order along x)");
    }    
    
    void shift_center() const throw() {
      // nothing to do for this se: should not be modified by a shift since it cannot accept only X shifts 
    }
    
    void compute_shifted() {
      // if the shift is on any dimension other than x, this would have been computed there
    }
    
    typedef unsigned int index_t;
    index_t begin_index, end_index;
    std::vector< std::pair<index_t, index_t> > vect_indexes;
    

    #ifndef NDEBUG
    const image_t& im;
    #endif
  
  };  
  
  
  
  
  

  /*! A runtime neighborhood (ie. a neighborhood that can be set at run time)
   *
   * @author Raffi Enficiaud
   */
  template <class image_t, class se_t_>
    struct s_runtime_neighborhood : 
      public INeighborhood, 
      public s_runtime_neighborhood_helper<typename se_t_::se_tag, image_t, se_t_>
  {
    typedef s_runtime_neighborhood<image_t, se_t_> this_type;
    typedef s_runtime_neighborhood_helper<typename se_t_::se_tag, image_t, se_t_> helper_t;


    typedef INeighborhood interface_type;
    typedef interface_type::const_iterator   interface_const_iterator;
    typedef interface_type::iterator         interface_iterator;
    typedef interface_type::coordinate_type  interface_coordinate_type;

    
    typedef typename image_t::coordinate_type    coordinate_type;
    
    
    
  private:
    typedef std::vector<offset> offset_storage_t;
    //typedef typename add_const<image_t_>::type    const_image_t;
    //typedef typename remove_const<image_t_>::type image_t;
    typedef typename helper_t::index_t index_t;
    
    
    // Voir avec boost.Intrusive au niveau des containers pour 
    // les listes de points filtrées. 
    
    
  public:
  
    typedef typename mpl::if_< 
      is_const<image_t>, 
      s_offset_list_iterator_const<typename offset_storage_t::const_iterator, image_t>,
      s_offset_list_iterator<typename offset_storage_t::const_iterator, image_t>
    >::type iterator;
  
    typedef s_offset_list_iterator_const<typename offset_storage_t::const_iterator, typename add_const<image_t>::type> const_iterator;
    
    s_runtime_neighborhood(image_t& im_, const se_t_& se) : 
      helper_t(im_, se),
      im(im_), 
      offset_max(total_number_of_points(im.Size())),
      o_shift(0),
      im_size(im.Size()),
      se_size(se.size()),
      coord_shifts(se.begin(), se.end()) // Raffi: pe. à mettre dans l'init car projection de se::coordinate_space à im::coordinate_space
    {
    
      yaRC res = initialise(se);
      if(res != yaRC_ok)
        throw errors::yaException(res);
    }
    
    
  private:
    yaRC initialise(const se_t_& se) {
      
      for(  typename se_t_::const_iterator it = se.begin(), ite = se.end();
            it != ite;
            ++it) 
      {
        offsets_shifts.push_back(from_coordinate_to_offset(im_size, *it));
      }
      offsets_shifts.resize(se.size() * 2); // in case a new list should be created
      offset_center.resize(offsets_shifts.size());
    
      return yaRC_ok;
    }
    
    
    
  protected:
    //! Centers the Neighborhood at a particular point
    virtual yaRC Center(const interface_coordinate_type& c) {
      return center(coordinate_type(c));
    }
    
    virtual yaRC Center(const interface_const_iterator& it) {
      throw center(coordinate_type(it->GetPosition()), it->GetOffset());
    }
    
    virtual yaRC Center(const offset o) {
      return center(o);
    }
    
    virtual yaRC SetShift(const interface_coordinate_type& c) {
      return set_shift(coordinate_type(c));
    }
      
    virtual yaRC ShiftCenter() {
      return shift_center();
    }
    
    
  public:
    //! Centers the neighborhood at the given point
    yaRC center(const coordinate_type& c) {
      DEBUG_ASSERT(is_point_inside(im_size, c), "The center point is outside the image");
      return center(c, from_coordinate_to_offset(im_size, c));
    }
    
    //! Centers the neighborhood at a given offset
    yaRC center(const offset o) {

      DEBUG_ASSERT(o >= 0, "The offset is negative (impossible for centering), offset value = " + any_to_string(o)); // we cannot tolerate negative offset there
          
      // test offset is inside the image or the window
      if(o > offset_max || o < 0)
        return yaRC_E_bad_parameters;
        
      return center(from_offset_to_coordinate(im_size, o), o);

    }
    
    /*! Centering using an iterator.
     * The iterator should implement the methods "Position" and "Offset", and this call saves
     * some computing comparatively to other centering methods (as efficient as "center(const coordinate_type& cc, const offset o)"
     * except safe_centering methods).
     *
     */
    template <class it_t>
    yaRC center(const it_t& it) {
      return center(it.Position(), it.Offset());
    }
    
    /*! Centering using both coordinate and offset information
     *  This is the most efficient centering method (all other centering methods call this method indirectly)
     */
    yaRC center(const coordinate_type& cc, const offset o) {
      // The helper decides the list on which to operate
      helper_t::center(o);
      
      // We crop the SE into the image
      typename helper_t::index_t new_begin = helper_t::begin_index, new_end = 0;
      for(typename helper_t::index_t i = helper_t::begin_index, j = helper_t::end_index; i < j; i++)
      {
        if(!is_point_inside(im_size, cc + coord_shifts[i])) {
          if(new_begin == helper_t::begin_index) {
            new_begin += se_size;
            for(typename helper_t::index_t ii = helper_t::begin_index; ii < i; ii++) {
              offset_center[se_size + ii] = offset_center[ii];
            }
          }
          continue;
        }
        offset_center[new_begin +  new_end++] = o + offsets_shifts[i];
      }
      
      if(new_begin != helper_t::begin_index) {
        helper_t::compute_shifted();
        // do the same for the shifted SE -> maybe should be implemented in the facade 
        // or some other concept extracted from it (depends on the current shift AND on the shift support of the SE). 
      }
      
      
      current_ = offset_center.begin() + new_begin;// + helper_t::begin_index;
      end_     = offset_center.begin() + new_begin + new_end;// + helper_t::begin_index;


      return yaRC_ok;
    
    }
    
    //! Centers the neighborhood at the given point whithout performing bounds checks
    yaRC safe_center(const coordinate_type& c) {
      // There is no call to any function of helper_t ?? --> false ...
      return safe_center(from_coordinate_to_offset(im_size, c));
    }
    
    /*! Centers the neighborhood at the given offset whithout performing bounds checks
     *
     * This method can be called when there is no collision between the actual neighborhood
     * and the bounds of the image.
     */
    yaRC safe_center(const offset o) {
      DEBUG_ASSERT(helper_t::begin_index >=0, "The begin indice is outside the current possible range");
      DEBUG_ASSERT(helper_t::end_index <= (std::max(offsets_shifts.size(), offset_center.size()) ), "The end indice is outside the current possible range : end_index= " + any_to_string(helper_t::end_index));
      
      helper_t::center(o);
      for(typename helper_t::index_t i = helper_t::begin_index, j = helper_t::end_index; i < j; i++)
      {
        offset_center[i] = o + offsets_shifts[i];
      }
      current_ = offset_center.begin() + helper_t::begin_index;
      end_     = offset_center.begin() + helper_t::begin_index + helper_t::end_index;      
      return yaRC_ok;
    }

    //! Sets the shift (the translation) between two successive calls to shift_center
    yaRC set_shift(const coordinate_type& c) {
      //helper_t::set_shift(c);
      return set_shift(from_coordinate_to_offset(im_size, c));
    }
    
    //! Sets the shift as an offset
    yaRC set_shift(const offset o) {
      helper_t::set_shift(o);
      o_shift = o;
      return yaRC_ok;
    }

    //! Returns the shift as an offset
    offset get_shift() const {
      return o_shift;
    }
    
    /*! Returns the covered and uncovered positions when the structuring element is shifted. Returns also the points that were moved from a position to another inside the 
     *  neighborhood.
     *
     */
    yaRC get_cover_uncover(offset shift, std::map<offset, offset> &cover, std::vector<offset> &new_covered, std::vector<offset> &uncovered) const 
    {
      cover.clear();
      new_covered.clear();
      uncovered.clear();
      
      for(typename offset_storage_t::const_iterator it(offset_center.begin()), ite(offset_center.end()); it != ite; ++it) {
        coordinate_type current_p = from_offset_to_coordinate_(im_size, *it + shift);
        for(typename offset_storage_t::const_iterator it2(offset_center.begin()), ite2(offset_center.end()); it2 != ite2; ++it2) {
          if(from_offset_to_coordinate_(im_size, *it2) == current_p) {
            DEBUG_ASSERT(cover.find(*it2) == cover.end(), "An previous element already exists at offset " + int_to_string(*it2));
            cover[*it2] = *it;
            break;
          }
        }
      }

      for(typename offset_storage_t::const_iterator it(offset_center.begin()), ite(offset_center.end()); it != ite; ++it) {
        offset shifted = *it + shift;
        
        if(cover.find(shifted) == cover.end()) {
          new_covered.push_back(*it);
        }
        else if(cover.find(*it) == cover.end()) {
          uncovered.push_back(*it);
        }
        
        DEBUG_ASSERT((cover.find(*it) == cover.end()) ^ (cover.find(shifted) == cover.end()), "Inconsistency in the covered and uncovered points");
        
      }      

      return yaRC_ok;
    }
        
    
    /*! Shifts the center of the neighborhood
     *
     */
    yaRC shift_center() {
      helper_t::shift_center();
      for(typename helper_t::index_t i = helper_t::begin_index, j = helper_t::end_index; i < j; i++)
      {
        offset_center[i] += o_shift;
      }
      return yaRC_ok;
    }
    
    const_iterator begin() const {
      return const_iterator(im, current_);
    }
    
    iterator begin() {
      return iterator(im, current_);
    }
    
    const_iterator end() const {
      return const_iterator(im, end_);
    }
    
    iterator end() {
      return iterator(im, end_);
    }    

    //!@group Virtual methods inherited from IObject
    //!@{
    //! Object type
    virtual type DynamicType() const {
      return type(type::c_neighborhood, type::s_object);
    }

    //! Object description
    virtual string_type Description() const {
      static const string_type s = "Generic structuring built on neighbor lists";
      return s;
    }
    //!@}


  protected:

    //! Const iteration over the neighborhood
    virtual interface_const_iterator BeginConst() const {
      return new const_iterator(begin());
    }
    virtual interface_const_iterator EndConst() const {
      return new const_iterator(end());
    }

    //! Iteration over the neighborhood
    virtual interface_iterator Begin() const {
      throw errors::yaException(yaRC_E_not_implemented);
    }
    virtual interface_iterator End() const {
      throw errors::yaException(yaRC_E_not_implemented);
    }
    
    
    
  private:
    image_t &im;
    const offset offset_max;
    offset o_shift;
    
    const coordinate_type im_size;
    const index_t se_size;
    const std::vector<coordinate_type> coord_shifts;
    
    
    offset_storage_t offsets_shifts, offset_center;
    typename offset_storage_t::iterator current_, end_;
    
  };



}}

#endif /* YAYI_RUNTIME_NEIGHBORHOOD_HPP__ */


