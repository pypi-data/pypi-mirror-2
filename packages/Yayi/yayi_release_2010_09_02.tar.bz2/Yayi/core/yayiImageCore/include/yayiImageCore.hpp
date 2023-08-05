/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_IMAGE_CORE_HPP__
#define YAYI_IMAGE_CORE_HPP__

/*! @file
 *  @brief Global definition for the image core library
 *
 */


#include <Yayi/core/yayiCommon/common_config.hpp>
#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiCommon/common_pixels.hpp>
#include <Yayi/core/yayiCommon/include/common_object.hpp>
#include <Yayi/core/yayiCommon/common_coordinates.hpp>
#include <Yayi/core/yayiCommon/common_variant.hpp>

#include <memory>


#ifdef YAYI_EXPORT_CORE_
#define YCor_ MODULE_EXPORT
#else
#define YCor_ MODULE_IMPORT
#endif



namespace yayi
{

  class IImage;
  class IIterator;
  class IConstIterator;




  /*!@brief A simple interface to special pixels returned by the interface layer of images
   *
   * @author Raffi Enficiaud
   */
  struct YCor_ IVariantProxy
  {
    typedef variant pixel_value_type;
    typedef IVariantProxy this_type;
  private:
    IVariantProxy& operator=(const IVariantProxy&);
    //{throw yayi::errors::yaException(yaRC_E_not_implemented);}

  public:
    virtual ~IVariantProxy() {}
    virtual IVariantProxy& operator=(const pixel_value_type& v)
    {
      setPixel(v);
      return *this;
    }

    pixel_value_type operator*() const
    {
      //throw yayi::errors::yaException(yaRC_E_not_implemented);
      return getPixel();
    }

    virtual bool operator==(const pixel_value_type&v) const
    {
      return isEqual(v);
    }
    virtual bool operator==(const this_type&v) const
    {
      return isEqual(v);
    }
        
    virtual bool operator!=(const pixel_value_type&v) const
    {
      return isDifferent(v);
    }
    virtual bool operator!=(const this_type&v) const
    {
      return isDifferent(v);
    }    
  //protected:
    
    virtual pixel_value_type getPixel () const = 0;
    virtual yaRC    setPixel          (const pixel_value_type &) = 0;
    virtual bool    isEqual           (const pixel_value_type &) const = 0;
    virtual bool    isEqual           (const this_type &) const = 0;
    virtual bool    isDifferent       (const pixel_value_type &) const = 0;
    virtual bool    isDifferent       (const this_type &) const = 0;
  };



  /*!@brief Image interface
   *
   * Main image interface
   * @author Raffi Enficiaud
   */
  class IImage : public IObject
  {
  public:
    typedef s_coordinate<0>                 coordinate_type;
    typedef offset                          offset_type;
    typedef variant                         pixel_value_type;
    typedef std::auto_ptr<IVariantProxy>    pixel_reference_type;
    
    typedef IIterator*                       iterator;
    typedef IConstIterator*                  const_iterator;

  public:
    virtual ~IImage(){}

    //! Images factory
    YCor_ static IImage*  Create(type, yaUINT8 dimension);

    //! Allocates the image
    //! The size should have been previously specified.
    virtual yaRC    AllocateImage()	= 0;

    virtual bool    IsAllocated()	const = 0;


    //! Frees the content of the image
    virtual	yaRC    FreeImage()			= 0;


    //!@group Size management
    //!@{
    //virtual coordinate_type&				Size()				= 0;
    //! Returns the actual size of the image
    virtual coordinate_type   GetSize() const	= 0;
    
    //! Changes the size of the image
    //! It is not possible to change the size when the image is allocated
    virtual yaRC              SetSize(const coordinate_type&)	= 0;
    
    //! Returns the dimension of the image
    virtual unsigned int      GetDimension() const = 0;
    //!@}


    //! Returns an iterator to the beginning of the image (the pixel's map)
    virtual iterator begin() throw() = 0;

    //! Returns an iterator to the end of the image (the pixel's map)
    virtual iterator end() throw() = 0;

    //! Returns a const iterator to the beginning of the image (the pixel's map)
    virtual const_iterator begin() const throw() = 0;

    //! Returns a const iterator to the end of the image (the pixel's map)
    virtual const_iterator end() const throw() = 0;

    //!@group Pixel access methods
    //!@{

    virtual pixel_value_type      pixel(const coordinate_type& ) const  = 0;
    virtual pixel_reference_type  pixel(const coordinate_type& )        = 0;

    //!@}



  };




  /*!@brief Iterator interface (const accesses)
   *
	 * Main image iterator interface with const access to the pixels of the image
	 * @author Raffi Enficiaud
   */
  class IConstIterator : public IObject
  {
  public:
    //! Type of the image on which the iteration is performed
    typedef IImage                            image_type;
    typedef image_type::coordinate_type       coordinate_type;
    typedef image_type::pixel_value_type      pixel_type;
    typedef IConstIterator                    this_type;

  public:
    //virtual ~IConstIterator(){} // not needed : IObject

    //! Returns true if the iterators refers to the same pixel
    virtual bool is_equal(const this_type* const& ) const = 0;

    //! Returns true if the iterators do not refer to the same pixel
    virtual bool is_different(const this_type* const& ) const = 0;

    //! Returns the actual position of the iterator
    virtual coordinate_type GetPosition() const throw() = 0;
    
    virtual offset          GetOffset() const throw() = 0;

    //! Set the actual position of the iterator
    virtual yaRC            SetPosition(const coordinate_type&) throw() = 0;
    
    //! Returns the value of the pixel
    virtual pixel_type      getPixel() const  = 0;

    //! Iterates to the next element
    virtual yaRC            next()            = 0;
    
    //! Iterates to the previous element
    virtual yaRC            previous()        = 0;
    
    //! Clones the current iterator
    virtual this_type*      clone() const     = 0;


  };
  
  

  /*!@brief Iterator interface with non const accesses
   *
   * Adds the pixels writing capabilities to the IConstIterator
   * @author Raffi Enficiaud
   */
  class IIterator //: public virtual IConstIterator
  {
  public:
    typedef IImage                            image_type;
    typedef image_type::pixel_value_type      pixel_type;
    typedef IIterator                         this_type;

    virtual ~IIterator(){}
    virtual yaRC      setPixel(const pixel_type&) = 0;
  };





} // namespace yayi

#endif

