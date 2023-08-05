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
#include <Yayi/core/yayiImageCore/yayiImageCoreFunctions.hpp>

#include <boost/python/class.hpp>
#include <boost/python/manage_new_object.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/iterator.hpp>


namespace yayi {
  IImage::pixel_reference_type::element_type* pixel_method_wrapper(IImage * im, const IImage::coordinate_type& c) {
    if(im == 0)
      throw errors::yaException(yaRC_E_null_pointer);
    
    IImage::pixel_reference_type v_ret = im->pixel(c);
    if(v_ret.get() == 0)
      throw errors::yaException(yaRC_E_allocation);

    return v_ret.release();
  }

  IIteratorWrapper image_range(IImage*im) {
    return IIteratorWrapper(im->begin(), im->end());
  }
  

}

void declare_image() {

  using namespace yayi;
  
  typedef IImage::pixel_reference_type (IImage::*pixel_non_const)(const IImage::coordinate_type&);
  typedef IImage::iterator (IImage::*iterator_non_const)();
  
  bpy::class_<IImage, bpy::bases<IObject>, boost::noncopyable >("Image", "Main image class", bpy::no_init)
    // size
    .add_property("Size",     &IImage::GetSize, &IImage::SetSize)
    .def("SetSize",           &IImage::SetSize,             "(dimension): sets the size of the image to the tuple 'dimension'")
    .def("GetSize",           &IImage::GetSize,             "returns the size of the image as a tuple")
    .def("GetDimension",      &IImage::GetDimension,        "returns the dimension of the support of the image")
    
    // allocation
    .def("IsAllocated",       &IImage::IsAllocated,        "returns true if the image is allocated")
    .def("AllocateImage",     &IImage::AllocateImage,      "allocates the image with the specified size")
    .def("FreeImage",         &IImage::FreeImage,          "free the content of the image (the size remains unchainged)")
    
    // information
    //.def("__str__",           &IImage::Description)
    //.def("DynamicType",       &IImage::DynamicType,        "provides information concerning the type of the image")
    
    // pixel
    //.def("pixel",             (pixel_non_const)&IImage::pixel,              "(coordinate): returns a reference to pixel at given coordinate")
    .def("pixel",
         &pixel_method_wrapper,        
         "(coordinate): provides a pointer to a pixel", 
         bpy::return_value_policy<bpy::manage_new_object, bpy::with_custodian_and_ward_postcall<0, 1> >())
    .add_property("pixels", 
      //bpy::range<>((iterator_non_const)&IImage::begin, (iterator_non_const)&IImage::end))
      //bpy::range<bpy::return_value_policy<bpy::copy_non_const_reference>/*, IIteratorWrapper*/>(&yayi::image_begin, &yayi::image_end))
      //bpy::range/*<bpy::return_value_policy<bpy::manage_new_object> >*/(iterator_non_const(&IImage::begin), iterator_non_const(&IImage::end))) // ok
      //bpy::range<bpy::return_value_policy<bpy::manage_new_object, bpy::with_custodian_and_ward_postcall<0,1> > >(iterator_non_const(&IImage::begin), iterator_non_const(&IImage::end)))

      //bpy::range/*<bpy::return_value_policy<bpy::copy_non_const_reference>, IImage* >*/(&yayi::image_begin, &yayi::image_end))
      
      // Raffi : this is a property ... 
      &yayi::image_range//,
      /*bpy::return_value_policy<bpy::with_custodian_and_ward_postcall<0,1> >()*/)


    
    // utilities
    //.def(bpy::self == bpy::other<IImage>())
    //.def(bpy::self != bpy::other<IImage>())    
    
  ;

  bpy::def("ImageFactory", 
    &IImage::Create, 
    "(type, dimension) : factory for images", 
    bpy::return_value_policy<bpy::manage_new_object>());
  
  bpy::def("GetSameImage", 
    (IImage* (*)(const IImage* const &im))&GetSameImage, 
    "(image) : returns a new image of the same type and dimension as the input", 
    bpy::return_value_policy<bpy::manage_new_object>());

  bpy::def("GetSameImageOf", 
    (IImage* (*)(const IImage* const &im, const yayi::type& t))&GetSameImage, 
    "(image, type) : returns a new image of the same dimension as the input, but with the type of pixels set to the input type", 
    bpy::return_value_policy<bpy::manage_new_object>());



}

