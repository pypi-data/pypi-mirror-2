/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiStructuringElementPython/structuringelement_python.hpp>
#include <boost/python/scope.hpp>
#include <boost/python/implicit.hpp>



void declare_se() {
  using namespace yayi;
  using namespace yayi::se;
  
  bpy::enum_<yayi::se::structuring_element_type>("structuring_element_type")
    .value("e_set_runtime",       yayi::se::e_set_runtime)
    .value("e_set_neighborlist",  yayi::se::e_set_neighborlist)
    .value("e_set_image",         yayi::se::e_set_image)
    .value("e_set_functional",    yayi::se::e_set_functional)
    
    .value("e_set_template",      yayi::se::e_set_template)
    .value("e_set_chain",         yayi::se::e_set_chain)
    .value("e_set_paired",        yayi::se::e_set_paired)
    
    .export_values()
    ;

  bpy::enum_<yayi::se::structuring_element_subtype>("structuring_element_subtype")
    .value("e_sest_neighborlist_generic_single",  yayi::se::e_sest_neighborlist_generic_single)
    .value("e_sest_neighborlist_hexa",            yayi::se::e_sest_neighborlist_hexa)
    .export_values()
    ;
  
  
  bpy::class_<IStructuringElement, bpy::bases<IObject>, boost::noncopyable >("StructuringElement", "Main structuring element class", bpy::no_init)
    // size
    .add_property("SEType",     &IStructuringElement::GetType)
    .def("GetSEType",           &IStructuringElement::GetType, "returns the type of the structuring element")

    .add_property("SETSubtype", &IStructuringElement::GetSubType)
    .def("GetSESubType",        &IStructuringElement::GetSubType, "returns the subtype of the structuring element")

        
    // information // already in IObject
    .def("Transpose",
         &IStructuringElement::Transpose,        
         "returns a new structuring element that is the transposed of this one", 
         bpy::return_value_policy<bpy::manage_new_object>())
         
    .def("RemoveCenter",
         &IStructuringElement::RemoveCenter,        
         "returns a new structuring element with the same shape, but without any center element", 
         bpy::return_value_policy<bpy::manage_new_object>())

    .add_property("Size",     &IStructuringElement::GetSize)
    
    .def("__eq__",                &IStructuringElement::is_equal)
    .def("__mod__",               &IStructuringElement::is_equal_unordered)
    .def("IsEqualUnordered",      &IStructuringElement::is_equal_unordered)
  ;
  
  bpy::def(
    "SEFactory", 
    &IStructuringElement::Create, 
    "factory for structuring elements", 
    bpy::return_value_policy<bpy::manage_new_object>());


}


