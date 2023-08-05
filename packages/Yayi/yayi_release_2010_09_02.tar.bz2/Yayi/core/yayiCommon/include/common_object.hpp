/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_OBJECT_HPP__
#define YAYI_COMMON_OBJECT_HPP__

#include <string>
#include <Yayi/core/yayiCommon/common_types.hpp>


namespace yayi
{
  /*!@brief Root object for interfaces
   * 
   * @author Raffi Enficiaud
   */
  class IObject
  {
  public:
    
    //! Destructor
    virtual ~IObject(){}

    //! Returns the current type of the object
    virtual type DynamicType() const              = 0;

    //! Object description
    virtual string_type Description() const       = 0;
  };



}
#endif /* YAYI_COMMON_OBJECT_HPP__ */

