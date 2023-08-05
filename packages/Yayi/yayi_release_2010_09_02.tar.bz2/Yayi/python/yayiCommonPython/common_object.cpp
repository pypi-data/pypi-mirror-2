/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/python/yayiCommonPython/common_python.hpp>
#include <Yayi/core/yayiCommon/include/common_object.hpp>


void declare_object() {
  using namespace yayi;

  bpy::class_<IObject, boost::noncopyable>("Object", "An abstract object", bpy::no_init)
    .def("DynamicType", &IObject::DynamicType, "type of the object")
    .def("Description", &IObject::Description, "description of the object") 
    .def("__str__",     &IObject::Description)
    ;

}

