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
#include <Yayi/core/yayiCommon/common_types.hpp>
#include <boost/python/enum.hpp>

// visual workaround
static std::string transform_to_string(const yayi::type& c)
{
  return c.operator yayi::string_type();
}


void declare_enums()
{

  bpy::enum_<yayi::type::scalar_type>("scalar_type")
    .value("s_ui8",   yayi::type::s_ui8)
    .value("s_ui16",  yayi::type::s_ui16)
    .value("s_ui32",  yayi::type::s_ui32)
    .value("s_ui64",  yayi::type::s_ui64)
    
    .value("s_i8",   yayi::type::s_i8)
    .value("s_i16",  yayi::type::s_i16)
    .value("s_i32",  yayi::type::s_i32)
    .value("s_i64",  yayi::type::s_i64)
    
    .value("s_float",  yayi::type::s_float)
    .value("s_double", yayi::type::s_double)

    .value("s_object", yayi::type::s_object)
    .value("s_variant",yayi::type::s_variant)
    .value("s_string", yayi::type::s_string)
    .value("s_wstring",yayi::type::s_wstring)
    .value("s_image",  yayi::type::s_image)

    .export_values()
    ;

  bpy::enum_<yayi::type::compound_type>("compound_type")
    .value("c_unknown",   yayi::type::c_unknown)
    .value("c_generic",   yayi::type::c_generic)
    .value("c_variant",   yayi::type::c_variant)
    .value("c_image",     yayi::type::c_image)
    
    .value("c_iterator",  yayi::type::c_iterator)
    .value("c_coordinate",yayi::type::c_coordinate)
    
    .value("c_scalar",    yayi::type::c_scalar)
    .value("c_complex",   yayi::type::c_complex)
    .value("c_3",         yayi::type::c_3)
    .value("c_4",         yayi::type::c_4)

    .value("c_vector",    yayi::type::c_vector)
    .value("c_map",       yayi::type::c_map)
    .value("c_container", yayi::type::c_container)
    .value("c_function",  yayi::type::c_function)

    .export_values()
    ;


  bpy::class_<yayi::type>("type", bpy::init<>())
    .def(bpy::init<yayi::type::compound_type, yayi::type::scalar_type>())
    .def_readwrite("c_type",    &yayi::type::c_type)
    .def_readwrite("s_type",    &yayi::type::s_type)
    .def(bpy::self == bpy::self)                                      // __eq__
    .def("__str__",             &transform_to_string)//&yayi::type::operator string_type)
    ;



}

