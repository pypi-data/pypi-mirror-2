/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYIIMAGEITERATOR_HPP__
#define YAYIIMAGEITERATOR_HPP__


#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageUtilities_T.hpp>

#include <boost/type_traits/add_const.hpp>
#include <boost/type_traits/remove_reference.hpp>
#include <boost/type_traits/add_reference.hpp>

namespace yayi
{

  template <class pixel_type_t, class coordinate_type_t>                          struct s_default_image_allocator;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>  class ImageIteratorWindowBase;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t>  class ImageIteratorContinuousBase;

  namespace {
 
    //! Iterator strategy based on the allocator (continuous vs. non continous maps)
    template <class pixel_type_t, class coordinate_type_t, class allocator_type>
      struct s_iterator_choice_strategy {
        // by default, we use the windowed iterator (the more generic)
        typedef ImageIteratorWindowBase<
          typename allocator_type::pixel_type,
          typename allocator_type::coordinate_type,
          allocator_type
        > type;
      };
    
    template <class pixel_type_t, class coordinate_type_t, class T1, class C1>
      struct s_iterator_choice_strategy  < pixel_type_t, coordinate_type_t, s_default_image_allocator<T1, C1> > {
        // the default image allcator allocate continous memory
        typedef ImageIteratorContinuousBase<
          pixel_type_t, 
          coordinate_type_t, 
          s_default_image_allocator<T1, C1>//pixel_type_t, coordinate_type_t> 
        > type;
      };
  }



  /*!@brief Main image non-windowed iterator type 
   *
   * @author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorContinuousBase : public IConstIterator
  {

  public:
    typedef ImageIteratorContinuousBase<
      pixel_type_t, 
      coordinate_type_t, 
      allocator_type_t>                                     this_type;
    typedef IConstIterator                                  interface_type;
    typedef coordinate_type_t                               coordinate_type;
    typedef interface_type::coordinate_type                 interface_coordinate_type;
    typedef interface_type::pixel_type                      interface_pixel_value_type;    
    typedef pixel_type_t                                    value_type;
    typedef typename add_pointer<value_type>::type          pointer_type;
    typedef typename add_reference<value_type>::type        reference;


    typedef std::bidirectional_iterator_tag                 iterator_category;

  private:
    pointer_type            p_;
    pointer_type            p_0;
    coordinate_type         grid_size;

    friend class ImageIteratorContinuousBase<
      typename boost::mpl::if_<boost::is_const<pixel_type_t>, typename boost::remove_const<pixel_type_t>::type, typename boost::add_const<pixel_type_t>::type>::type, 
      coordinate_type_t, 
      allocator_type_t>;

  public:
    //! Default constructor
    ImageIteratorContinuousBase() : p_(0), p_0(0), grid_size() {}

    //! Constructor from image information
    ImageIteratorContinuousBase(
      value_type&             initial_pixel,
      const coordinate_type&  init_coord, 
      const coordinate_type&  grid_size_, 
      const coordinate_type&  , 
      const coordinate_type&  ) : p_(&initial_pixel + from_coordinate_to_offset(grid_size_, init_coord)), p_0(&initial_pixel), grid_size(grid_size_)
    {}
    
    //! Template constructor from another type
    template <typename v_type>
    ImageIteratorContinuousBase(
      const ImageIteratorContinuousBase<v_type, coordinate_type_t, allocator_type_t>& it) : 
        p_(it.p_), p_0(it.p_0), grid_size(it.grid_size)
    {}

    //! Advance the iterator to the next position
    this_type& operator++() 
    {
      ++p_;
      return *this;
    }

    //! Advance the iterator to the previous position
    this_type& operator--() 
    {
      --p_;
      return *this;
    }

    //! Comparison operator
    bool operator==(const this_type& r) const throw()
    {
      return p_ == r.p_;
    }

    bool operator!=(const this_type& r) const throw()
    {
      return p_ != r.p_;
    }

    //! Position
    coordinate_type Position() const
    {
      return from_byte_offset_to_coordinate<coordinate_type, pixel_type_t>(
        grid_size, 
        reinterpret_cast<const unsigned char*>(p_) - reinterpret_cast<const unsigned char*>(p_0));
    }
    
    offset Offset() const {
      return p_ - p_0;
    }


    //! Dereference operator
    reference operator*() const
    {
      DEBUG_ASSERT(p_ < p_0 + total_number_of_points(grid_size) , "Trying to deference an iterator after the end of the image");
      return *p_;
    }



    //!@group IIterator interface methods
    //!@{
    //! Position retrieval (@ref IIterator interface)
    virtual interface_coordinate_type GetPosition() const throw()
    {
      return interface_coordinate_type(Position());
    }
    
    virtual offset GetOffset() const throw() {
      return Offset();
    }

    //! @TODO : implement this method (since it is rather easy)
    virtual yaRC SetPosition(const interface_coordinate_type&) throw()
    {
      return yaRC_E_not_implemented;
    }

    virtual bool is_equal(const interface_type* const& it_interface) const
    {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("Unable to compare iterators of different kind");
      return (*this) == (*it_);
    }
    virtual bool is_different(const interface_type* const& it_interface) const
    {
      const this_type* it_ = dynamic_cast<const this_type*>(it_interface);
      if(!it_)
        throw yayi::errors::yaException("Unable to compare iterators of different kind");
      return (*this) != (*it_);
    }

    virtual type DynamicType () const
    {
      //@todo proper type setting
      static const type t(type::c_iterator, type::s_image);
      return t;
    }

    virtual string_type Description() const
    {
      return "Continuous iterator";
    }

    //!@}
    
  protected:
    virtual interface_pixel_value_type getPixel() const {
      //std::cout << "IConstIterator::getPixel p_ = " << (void*)p_ << std::endl;
      return interface_pixel_value_type(*p_);
    }

    virtual yaRC next() {
      this->operator++();
      return yaRC_ok;
    }
    virtual yaRC previous() {
      this->operator--();
      return yaRC_ok;
    }
    virtual this_type* clone() const throw() {
      // this works because the children classes do not have special copy constructors ?
      return new this_type(*this);
    }

  };





  /*!@brief Main image windowed iterator type 
   *
   * @author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorWindowBase : public IConstIterator
  {


  public:
    typedef ImageIteratorWindowBase<
      pixel_type_t, 
      coordinate_type_t, 
      allocator_type_t>                                     this_type;
    typedef IConstIterator                                  interface_type;
    typedef coordinate_type_t                               coordinate_type;
    typedef interface_type::coordinate_type                 interface_coordinate_type;
    typedef interface_type::pixel_type                      interface_pixel_value_type;    
    typedef pixel_type_t                                    value_type;
    typedef typename add_reference<value_type>::type        reference;
    typedef typename add_pointer<pixel_type_t>::type        pointer_type;

    typedef std::bidirectional_iterator_tag                 iterator_category;

  private:
    pointer_type  p_;
    pointer_type  p_0;

    coordinate_type                                         coord, grid_size;
    coordinate_type                                         window_begin, window_end;

    friend class ImageIteratorWindowBase<
      typename boost::mpl::if_<boost::is_const<pixel_type_t>, typename boost::remove_const<pixel_type_t>::type, typename boost::add_const<pixel_type_t>::type>::type, 
      coordinate_type_t, 
      allocator_type_t>;


  public:
    
    //! Default constructor
    ImageIteratorWindowBase() : 
      p_(0), p_0(0), coord(), grid_size(), window_begin(), window_end()
    {}

    //! Constructor
    ImageIteratorWindowBase(
      reference               initial_pixel,
      const coordinate_type&  init_coord, 
      const coordinate_type&  grid_size_, 
      const coordinate_type&  window_begin_, 
      const coordinate_type&  window_size_) : 
        p_(&initial_pixel + from_coordinate_to_offset(grid_size_, init_coord)),
        p_0(&initial_pixel), 
        coord(init_coord), grid_size(grid_size_), 
        window_begin(window_begin_), window_end(window_begin_+window_size_)
    {
      // assert coord is inside
    }

    //! Template constructor from another type
    template <typename v_type>
    ImageIteratorWindowBase(
      const ImageIteratorWindowBase<v_type, coordinate_type_t, allocator_type_t>& it) : 
        p_(it.p_), p_0(it.p_0), 
        coord(it.coord), 
        grid_size(it.grid_size),
        window_begin(it.window_begin), window_end(it.window_end)
    {}


    //! Advance the iterator to the next position
    this_type& operator++() 
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0, j = coord.dimension(); i < j; i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        current++;
        if(current < window_end[i])
        {
          p_++;
          break;
        }

        // ici ajout padding ?
        if(i == coord.dimension() - 1)
          break;

        current = window_begin[i];
        p_ += hyperplan_size*(grid_size[i] - (window_end[i] - current)); // Raffi : +1 ?? je ne sais jamais... à tester
        hyperplan_size *= grid_size[i];
      }


      return *this;
    }

    //! Advance the iterator to the next position
    this_type& operator--() 
    {
      offset hyperplan_size = 1;
      for(unsigned int i = 0; i < coord.dimension(); i ++)
      {
        typename coordinate_type::scalar_coordinate_type& current = coord[i];
        current--;
        if(current >= window_begin[i])
        {
          p_--;
          break;
        }
        if(i == coord.dimension() - 1)
          break;
        
        // ici ajout padding ?
        current = window_end[i]-1;
        p_ -= hyperplan_size*(grid_size[i] - (current - window_begin[i])); // Raffi : +1 ?? je ne sais jamais... à tester
        hyperplan_size *= grid_size[i];
      }
      return *this;
    }


    //! Dereference operator
    reference operator*() const
    {
      DEBUG_ASSERT(p_ < p_0 + total_number_of_points(grid_size) , "Trying to deference an iterator after the end of the image");
      return *p_;
    }


    //! Comparison operator
    bool operator ==(const this_type& r) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(r.window_begin == window_begin && r.window_end == window_end && grid_size == r.grid_size, "Comparison between incompatible iterators (different ranges)");
      return coord == r.coord;
    }

    bool operator !=(const this_type& r) const YAYI_THROW_DEBUG_ONLY__
    {
      DEBUG_ASSERT(r.window_begin == window_begin && r.window_end == window_end && grid_size == r.grid_size, "Comparison between incompatible iterators (different ranges)");
      return coord != r.coord;
    }

    const coordinate_type& Position() const
    {
      return coord;
    }
    offset Offset() const {
      return p_ - p_0;
    }    

    virtual interface_coordinate_type GetPosition() const throw()
    {
      return interface_coordinate_type(Position());
    }
    virtual yaRC SetPosition(const interface_coordinate_type&) throw()
    {
      return yaRC_E_not_implemented;
    }
    virtual offset GetOffset() const throw() {
      return Offset();
    }


    //!@group IIterator interface methods
    //!@{
    virtual bool is_equal(const interface_type*const& it_interface) const throw()
    {
      const this_type* it_this = dynamic_cast<const this_type*>(it_interface);
      if(!it_this)
        return false;
      return this->operator ==(*it_this);
    }
    virtual bool is_different(const interface_type*const& it_interface) const throw()
    {
      const this_type* it_this = dynamic_cast<const this_type*>(it_interface);
      if(!it_this)
        return true;
      return this->operator !=(*it_this);
    }

    virtual type DynamicType() const
    {
      //@todo proper type setting
      static const type t(type::c_iterator, type::s_image);
      return t;
    }

    virtual string_type Description() const
    {
      return "Hyperrectangle iterator";
    }

    //!@}

  protected:
    virtual interface_pixel_value_type getPixel() const {
      return interface_pixel_value_type(value_type(0));
    }
    virtual yaRC next() {
      this->operator++();
      return yaRC_ok;
    }
    virtual yaRC previous() {
      this->operator--();
      return yaRC_ok;
    }
        
    virtual this_type* clone() const throw() {
      // this works because the children classes do not have special copy constructors ?
      return new this_type(*this);
    }
  };


  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorNonWindowed;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorNonWindowedConst;


  /*!@brief Non windowed iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorNonWindowed : 
    public s_iterator_choice_strategy<pixel_type_t, coordinate_type_t, allocator_type_t>::type,
    public IIterator
  {
    typedef typename s_iterator_choice_strategy<pixel_type_t, coordinate_type_t, allocator_type_t>::type parent_type;
    //friend class ImageIteratorNonWindowedConst<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>;

  public:
    typedef typename parent_type::coordinate_type             coordinate_type;
    typedef typename parent_type::reference                   reference;
    typedef typename parent_type::value_type                  value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;

  public:
    //! Constructor from image information
    ImageIteratorNonWindowed(
      reference               initial_pixel,
      const coordinate_type&  init_coord, 
      const coordinate_type&  grid_size_, 
      const coordinate_type&  window_begin_, 
      const coordinate_type&  window_size_) : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    //! Default constructor
    ImageIteratorNonWindowed() : parent_type()
    {}

    reference operator*() const
    {
      return this->parent_type::operator*();
    }
    
    
  protected:
    virtual yaRC setPixel(const interface_pixel_value_type& v) {
      this->operator*() = v.operator value_type();
      return yaRC_ok;
    }

  };


  /*!@brief Non windowed const iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorNonWindowedConst : 
    public s_iterator_choice_strategy<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>::type
  {
    typedef typename s_iterator_choice_strategy<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>::type parent_type;

  public:
    typedef typename parent_type::coordinate_type             coordinate_type;
    typedef typename 
      boost::add_reference<
        typename boost::add_const<
          typename boost::remove_reference<typename parent_type::reference>::type
          >::type
        >::type reference;
    typedef typename parent_type::value_type                  value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;
    
  public:
    //! Default constructor
    ImageIteratorNonWindowedConst() : parent_type() {}

    //! Constructor from image information
    ImageIteratorNonWindowedConst(
      reference               initial_pixel,
      const coordinate_type&  init_coord, 
      const coordinate_type&  grid_size_, 
      const coordinate_type&  window_begin_, 
      const coordinate_type&  window_size_) : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}
    
    //! Constructor from non const similar iterator
    template <class pix_t>
    ImageIteratorNonWindowedConst(
      ImageIteratorNonWindowed<pix_t, coordinate_type_t, allocator_type_t> const& it) : 
        parent_type(/*static_cast<typename ImageIteratorNonWindowed<pixel_type_t, coordinate_type_t, allocator_type_t>::parent_type const&>(*/it/*)*/)
    {}

    reference operator*() const
    {
      return this->parent_type::operator*();
    }
  };


  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorWindowed;
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorWindowedConst;

  /*!@brief Windowed iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorWindowed : 
    public ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t>,
    public IIterator
  {
    typedef ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t> parent_type;
    //friend class ImageIteratorWindowedConst<typename boost::add_const<pixel_type_t>::type, coordinate_type_t, allocator_type_t>;
  
  public:
    typedef typename parent_type::coordinate_type coordinate_type;
    typedef typename parent_type::reference       reference;
    typedef typename parent_type::value_type      value_type;
    typedef typename parent_type::interface_pixel_value_type  interface_pixel_value_type;

  public:
    ImageIteratorWindowed(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_, 
      const coordinate_type&  window_begin_, 
      const coordinate_type&  window_size_) : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}

    reference operator*() const
    {
      return this->parent_type::operator*();
    }

  protected:
    virtual yaRC setPixel(const interface_pixel_value_type& v) {
      this->operator*() = v.operator value_type();
      return yaRC_ok;
    }

  };

  /*!@brief Windowed const iterator
   *
   *@author Raffi Enficiaud
   */
  template <class pixel_type_t, class coordinate_type_t, class allocator_type_t> 
  class ImageIteratorWindowedConst : 
    public ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t>
  {
    typedef ImageIteratorWindowBase<pixel_type_t, coordinate_type_t, allocator_type_t> parent_type;

  public:
    typedef typename parent_type::coordinate_type coordinate_type;
    //typedef typename parent_type::reference  reference;
    typedef typename 
      boost::add_reference<
        typename boost::add_const<
          typename boost::remove_reference<typename parent_type::reference>::type
          >::type
        >::type reference;
    typedef typename parent_type::value_type      value_type;

  public:
    ImageIteratorWindowedConst(
      reference               initial_pixel,
      const coordinate_type&  init_coord,
      const coordinate_type&  grid_size_, 
      const coordinate_type&  window_begin_, 
      const coordinate_type&  window_size_) : parent_type(initial_pixel, init_coord, grid_size_, window_begin_, window_size_)
    {}
    
    //! Constructor from non const similar iterator
    template <class pix_t>
    ImageIteratorWindowedConst(
      ImageIteratorWindowed<pix_t, coordinate_type_t, allocator_type_t> const& it) : 
        parent_type(it)
    {}    

    reference operator*() const
    {
      return this->parent_type::operator*();
    }
  };


}


#endif

