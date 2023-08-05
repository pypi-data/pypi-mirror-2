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

// reference to an internal structure of yayiImageCorePython
#include <Yayi/python/yayiImageCorePython/imagecore_python.hpp>

using namespace yayi;
using namespace yayi::se;

IConstIteratorWrapper neighbor_range(IConstNeighborhood*n) {
  return IConstIteratorWrapper(n->BeginConst(), n->EndConst());
}


void declare_neighbor_factory() {
 
      
  bpy::class_<IConstNeighborhood, bpy::bases<IObject>, boost::noncopyable >(
    "ConstNeighborhood", 
    "Main const neighborhood class. This class does not allow any writing into the image", bpy::no_init)
    
    // size
    .def("Center",            (yaRC (IConstNeighborhood::*)(const IConstNeighborhood::coordinate_type&))  &IConstNeighborhood::Center, "centers the structuring element at the specified coordinate")
    .def("Center",            (yaRC (IConstNeighborhood::*)(const IConstNeighborhood::const_iterator&))   &IConstNeighborhood::Center, "centers the structuring element at the specified iterator position")
    .def("Center",            (yaRC (IConstNeighborhood::*)(const offset))                                &IConstNeighborhood::Center, "centers the structuring element at the specified offset")

    .def("SetShift",          &IConstNeighborhood::SetShift,            "specifies the shift that will be later applied to the center")
    .def("ShiftCenter",       &IConstNeighborhood::ShiftCenter,         "shifts the center by a shift previously defined")
    
    .add_property("pixels", neighbor_range)
        
    // information
    //.def("__str__",           &IStructuringElement::Description)
    //.def("DynamicType",       &IStructuringElement::DynamicType,        "provides information concerning the type of the image")
    //.add_property("Type",     &IConstNeighborhood::DynamicType)
    
  ;
  bpy::def("NeighborhoodFactory", &IConstNeighborhood::Create, "factory for the neighborhood", bpy::return_value_policy<bpy::manage_new_object>());
}

