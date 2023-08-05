/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_STRUCTURING_ELEMENT_MAIN_HPP__
#define YAYI_STRUCTURING_ELEMENT_MAIN_HPP__





/*@namespace structuring
 *@brief Structuring element structures and elements
 *
 *
 *@author Raffi Enficiaud
 */



#include <Yayi/core/yayiCommon/common_config.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>


#ifdef YAYI_EXPORT_SE_
#define YSE_ MODULE_EXPORT
#else
#define YSE_ MODULE_IMPORT
#endif


namespace yayi {

  namespace se {


    typedef enum e_structuring_element_type {
      e_set_runtime,
      e_set_neighborlist,                       //!< Neighborlist structuring element
      e_set_image,                              //!< Image structuring element
      e_set_functional,
      e_set_template,                           //!< Complete template type of structuring element (cannot be used for dynamic definition, eg. for internal use)
      e_set_chain,                              //!< Chain of structuring element
      e_set_paired
    
    } structuring_element_type;


    typedef enum e_structuring_element_subtype {
      e_sest_neighborlist_generic_single,       //!< generic single list structuring element
      e_sest_neighborlist_hexa                  //!< hexagonal reshaping structuring element
    } structuring_element_subtype;


    /*! Interface for structuring elements
     *  @author Raffi Enficiaud
     */
    class IStructuringElement : public IObject {
    public:
      virtual ~IStructuringElement(){}

      //! Returns a new structuring element that is a transposed copy of this one
      virtual IStructuringElement* Transpose() const    = 0;

      //! Returns the runtime type of the structuring element (see @ref structuring_element_type)
      virtual structuring_element_type GetType() const  = 0;
      
      //! Returns the subtype of the structuring element (see @ref structuring_element_subtype)
      virtual e_structuring_element_subtype GetSubType() const  = 0;
      
      //! Removes the center point from the structuring element
      //! (usually useful for propagating algorithms, hit-or-miss etc.)
      virtual IStructuringElement* RemoveCenter() const = 0;
      
      //! Returns the size of the structuring element in number of neighbors (the center, if defined, is included)
      //! @todo: Raffi: maybe should be a property of a special kind of structuring elements only
      virtual unsigned int GetSize() const              = 0;

      //! Returns a copy of this structuring element
      virtual IStructuringElement* Clone() const        = 0;
      
      //! Checks the equality this structuring element with the provided one
      virtual bool is_equal(const IStructuringElement* ) const throw() = 0;
      
      //! Checks the equality of the structuring element with the argument, but without considering any ordering information about the
      //! elements of the structuring elements.
      virtual bool is_equal_unordered(const IStructuringElement* se) const throw() = 0;
      
      /*! Structuring element factory
       * Create a structuring element of the give type, subtype and dimension, using the provided shape element
       * The shape element can be a list of coordinates, an image or a function supported by the variant definition (unary function of coordinate returning coordinates).
       *
       * The only supported shape structure is currently the list of displacement from the center
       *
       */
      static YSE_ IStructuringElement* Create(structuring_element_type se_t, yaUINT8 dimension, const variant& shape_element, structuring_element_subtype se_sub_t = e_sest_neighborlist_generic_single);
      
    };
    
    
    
    /*! Interface for the neighborhood
     *  @author Raffi Enficiaud
     */
    class IConstNeighborhood : public IObject {
    public:
      virtual ~IConstNeighborhood(){}
    
      //! The iterator type for the neighborhood (generic image iterator interface)
      typedef IImage                                image_type;
      typedef image_type::coordinate_type           coordinate_type;
      typedef IIterator*                            iterator;
      typedef IConstIterator*                       const_iterator;
      
      //! Centers the Neighborhood at a particular point
      virtual yaRC Center(const coordinate_type&) = 0;
      
      //! Centers the neighborhood at the point defined by the iterator
      virtual yaRC Center(const const_iterator&) = 0;

      //! Centers the neighborhood at the point defined by the iterator
      virtual yaRC Center(const offset) = 0;
           
      /*!This function defines the shift between two successive calls to 
       * the center method. 
       */
      virtual yaRC SetShift(const coordinate_type&) = 0;
      
      /*! Shifts the centers of the neighborhood with an offset defined 
       *  by the call to @ref set_shift.
       */
      virtual yaRC ShiftCenter() = 0;
      
      //! Returns a const iterator to the beginning of the neighborhood
      virtual const_iterator BeginConst() const = 0;
      
      //! Returns a const iterator to the end of the neighborhood
      virtual const_iterator EndConst()   const = 0;      
      
      //! Factory for the structuring element
      static YSE_ IConstNeighborhood* Create(const IImage&, const IStructuringElement&);
    };


    /*! Interface for the neighborhood (with write accesses)
     *  @author Raffi Enficiaud
     */  
    class INeighborhood : public IConstNeighborhood {
    public:
  
      virtual iterator Begin() const = 0;
      virtual iterator End()   const = 0;      
      
      //! Factory for the structuring element
      static YSE_ INeighborhood* Create(IImage&, const IStructuringElement&);  
    };
  
  
  
  
    /*!@brief Creates a neighborlist structuring element as a ball of given radius and using given metric
     *
     * @param[in] dimension the dimension of the resulting structuring element
     * @param[in] metric    the "power" of the metric used for the ball. O or negative or Nan stands for infinity (max) metric
     * @param[in] radius    the radius of the desired ball
     * @result a single list neighborlist structuring element
     *
     * @author Raffi Enficiaud
     */
    YSE_ IStructuringElement * CreateBallSE(yaUINT8 dimension, const yaUINT8 metric, const double radius);
  
  }
}



#endif

