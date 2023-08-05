/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/python/yayiImageCorePython/imagecore_python.hpp>

#include <boost/python/class.hpp>
#include <boost/python/manage_new_object.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/lambda/lambda.hpp>

#if 0
namespace boost { namespace python
{
  template <class C>
  struct iterators<>
  {
      typedef typename C::[const_]iterator iterator;
      static iterator begin(C& x);
      static iterator end(C& x);
  };
}}
#endif

namespace yayi {


    
  IConstIteratorWrapper ItClone(const IConstIteratorWrapper&it) {return IConstIteratorWrapper(it);}

  IConstIterator::coordinate_type GetPosition(const IConstIteratorWrapper& it)
  {
    return it.ptr()->GetPosition();
  }
  yaRC SetPosition(IConstIteratorWrapper& it, const IConstIterator::coordinate_type& c)
  {
    return it.ptr()->SetPosition(c);
  }
}



void declare_iterators() {

  using namespace yayi;
  //using namespace boost::lambda;
  
  bpy::class_<IConstIteratorWrapper, bpy::bases<IObject> >("ConstIterator", "Const iterator over a range on images", bpy::no_init)
    .def("__iter__",    &ItClone, bpy::with_custodian_and_ward_postcall<0,1> () )
  
    .def("next",        &IConstIteratorWrapper::next)
    .def("previous",    &IConstIteratorWrapper::previous)

    .def(bpy::self == bpy::other<IConstIteratorWrapper>())
    .def(bpy::self != bpy::other<IConstIteratorWrapper>())

    .def("GetPosition",           &GetPosition)//boost::lambda::protect(_1.ptr()->GetPosition))
    .def("SetPosition",           &SetPosition)
    .add_property("position",     &GetPosition, &SetPosition)

    .def("GetPixel",          &IConstIteratorWrapper::getPixel)
    .add_property("value",    &IConstIteratorWrapper::getPixel)
    
    .def("has_next",          &IConstIteratorWrapper::has_next)
  ;
    
  
  bpy::class_<IIteratorWrapper, bpy::bases<IConstIteratorWrapper> >("Iterator", "Iterator over a range on images", bpy::no_init)
    .def("__iter__",          &ItClone, bpy::with_custodian_and_ward_postcall<0,1> () )
    .def("SetPixel",          &IIteratorWrapper::setPixel)
    .add_property("value",    &IIteratorWrapper::getPixel, &IIteratorWrapper::setPixel)

  ;  
  
}
