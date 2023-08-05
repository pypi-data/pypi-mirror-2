/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#if YAYI_IO_NUMPY_ENABLED__


#include <Yayi/python/yayiIOPython/io_python.hpp>
#include <numpy/ndarrayobject.h> // interface to numpy
#include <Yayi/core/yayiCommon/include/common_dispatch.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_ImplDispatch.hpp>

#include <boost/python/handle.hpp> 

using namespace yayi;
using namespace yayi::IO;

template <class pixel_t>
struct s_to_numpy_helper {};

template <> struct s_to_numpy_helper<yaUINT8>   {enum {e_num_t =  NPY_UINT8};};
template <> struct s_to_numpy_helper<yaINT8>    {enum {e_num_t =  NPY_INT8};};
template <> struct s_to_numpy_helper<yaUINT16>  {enum {e_num_t =  NPY_UINT16};};
template <> struct s_to_numpy_helper<yaINT16>   {enum {e_num_t =  NPY_INT16};};
template <> struct s_to_numpy_helper<yaUINT32>  {enum {e_num_t =  NPY_UINT32};};
template <> struct s_to_numpy_helper<yaINT32>   {enum {e_num_t =  NPY_INT32};};
template <> struct s_to_numpy_helper<yaUINT64>  {enum {e_num_t =  NPY_UINT64};};
template <> struct s_to_numpy_helper<yaINT64>   {enum {e_num_t =  NPY_INT64};};
template <> struct s_to_numpy_helper<yaF_simple>{enum {e_num_t =  NPY_FLOAT};};
template <> struct s_to_numpy_helper<yaF_double>{enum {e_num_t =  NPY_DOUBLE};};



template <class image_t>
PyObject* get_new_numpyarray_around_existing_image(yayi::IImage* iim)
{
  image_t * im = dynamic_cast<image_t*> (iim);
  if(im == 0)
    return 0;
  
  typedef typename image_t::coordinate_type coordinate_type;
  npy_intp dims[coordinate_type::static_dimensions];
  for(unsigned int i = 0; i < coordinate_type::static_dimensions; i++) dims[coordinate_type::static_dimensions - i - 1] = im->Size()[i];
  return PyArray_SimpleNewFromData(coordinate_type::static_dimensions, dims, s_to_numpy_helper<typename image_t::pixel_type>::e_num_t, &(im->pixel(0)));
  
}



bpy::handle<PyObject> image_to_numpy(yayi::IImage* im)
{
  //std::cout << "image_to_numpy 1" << std::endl;
  yaRC res;
  PyObject *return_value;
    
  if(im == 0)
    return 0;

  yayi::dispatcher::s_dispatcher<PyObject*, IImage*> dispatch_object(return_value, im);

  res = dispatch_object.calls_first_suitable(
          fusion::vector_tie(
          get_new_numpyarray_around_existing_image< Image<yaUINT8> >,
          get_new_numpyarray_around_existing_image< Image<yaUINT16> >,
          get_new_numpyarray_around_existing_image< Image<yaUINT32> >,
          get_new_numpyarray_around_existing_image< Image<yaUINT64> >,
          
          get_new_numpyarray_around_existing_image< Image<yaINT8> >,
          get_new_numpyarray_around_existing_image< Image<yaINT16> >,
          get_new_numpyarray_around_existing_image< Image<yaINT32> >,
          get_new_numpyarray_around_existing_image< Image<yaINT64> >
          ));

  //std::cout << "image_to_numpy 2 : res = " << res  << std::endl;
  //std::cout << "image_to_numpy 3 : ret = " << (void*)return_value << std::endl;

  if(res == yaRC_ok)
    return bpy::handle<PyObject>(return_value);
  else if(res != yaRC_E_not_implemented)
  {
    throw errors::yaException(res);
    //return bpy::handle<PyObject>(bpy::allow_null<PyObject>(0));
  }

  res = dispatch_object.calls_first_suitable(
          fusion::vector_tie(
          get_new_numpyarray_around_existing_image< Image<yaF_simple> >,
          get_new_numpyarray_around_existing_image< Image<yaF_double> >
        ));

  if(res == yaRC_ok)
    return bpy::handle<PyObject>(return_value);
  throw errors::yaException(res);
  //else if(res != yaRC_E_not_implemented)
  //  return bpy::handle<PyObject>(bpy::allow_null<PyObject>(0));
}

template <class image_t>
yaRC create_and_fill_image(PyObject* array, IImage*& iimout)
{
  typedef typename image_t::coordinate_type coordinate_type;
  typedef typename image_t::pixel_type pixel_type;

  
  image_t& imout = dynamic_cast<image_t&>(*iimout);
  coordinate_type size(0);
  for(int current_dim = 0; current_dim < coordinate_type::static_dimensions; current_dim++)
  {
    npy_intp s = PyArray_DIM(array, current_dim); 
    size[coordinate_type::static_dimensions - current_dim - 1] = s; // reversed order
  }

  yaRC res = imout.SetSize(size);
  if(res != yaRC_ok)
  {
    delete iimout;
    iimout = 0;
    return res;
  }
  
  res = imout.AllocateImage();
  if(res != yaRC_ok)
  {
    delete iimout;
    iimout = 0;
    return res;
  }
  
  

  PyObject* array_iter = PyArray_IterNew(array);
  bpy::handle<> boost_iter_handler(array_iter); // for proper destructor managment, but slows the access
  for(typename image_t::iterator it(imout.begin_block()), ite(imout.end_block()); 
      (it != ite) && (PyArray_ITER_NOTDONE(array_iter) != 0); 
      ++it)
  {
    void * p_data = PyArray_ITER_DATA(array_iter);
    *it = *static_cast<typename image_t::pixel_type*>(p_data);
    PyArray_ITER_NEXT(array_iter);
  }
  
  
  return yaRC_ok;

}


template <class pixel_type>
yaRC from_numpy_array_to_image(PyObject* array, IImage*& iimout)
{
  typedef type_support<pixel_type> ts;
  
  // test if array is numpy !
  
  if(iimout != 0)
    return yaRC_E_not_null_pointer;
  
  int dim = PyArray_NDIM(array);  
  iimout = IImage::Create(yayi::type(ts::compound, ts::scalar), dim);
  if(iimout == 0)
    return yaRC_E_unknown;

  switch(dim)
  {
  case 2:
  {
    typedef Image<pixel_type, s_coordinate<2> > image_t;
    return create_and_fill_image<image_t>(array, iimout);
  }
  case 3:
  {
    typedef Image<pixel_type, s_coordinate<3> > image_t;
    return create_and_fill_image<image_t>(array, iimout);
  }
  case 4:
  {
    typedef Image<pixel_type, s_coordinate<4> > image_t;
    return create_and_fill_image<image_t>(array, iimout);
  }  
  default:
    DEBUG_INFO("Unsupported array dimension");
    delete iimout;
    iimout = 0;
    return yaRC_E_not_implemented;
  }
}



yayi::IImage* image_from_numpy(PyObject* array)
{
  // test if array is numpy !
  if(!PyArray_Check(array))
  {
    throw errors::yaException("The input array does not seem to be numpyarray compatible");
  }

  int array_type = PyArray_TYPE(array);
  yayi::IImage* out = 0;
  yaRC res;
  
  switch(array_type)
  {
  case NPY_UINT8:  res = from_numpy_array_to_image<yaUINT8>(array, out); break;
  case NPY_UINT16: res = from_numpy_array_to_image<yaUINT16>(array, out); break;
  case NPY_UINT32: res = from_numpy_array_to_image<yaUINT32>(array, out); break;
   
  case NPY_INT8:  res = from_numpy_array_to_image<yaINT8>(array, out); break;
  case NPY_INT16: res = from_numpy_array_to_image<yaINT16>(array, out); break;
  case NPY_INT32: res = from_numpy_array_to_image<yaINT32>(array, out); break;
  
  case NPY_FLOAT:  res = from_numpy_array_to_image<yaF_simple>(array, out); break;
  case NPY_DOUBLE: res = from_numpy_array_to_image<yaF_double>(array, out); break;
  
  default:
    DEBUG_INFO("Unknown array type");
    //return yaRC_E_not_implemented;
  }

  if(out == 0 || res != yaRC_ok)
  {
    throw errors::yaException("An error occured while converting the array into an image" + (res != yaRC_ok ? std::string(res) : "unimplemented method"));
  }
  return out;
}

void declare_numpy() {

  import_array();
  boost::python::numeric::array::set_module_and_type("numpy", "ndarray");

  bpy::def( "image_to_numpy", 
            image_to_numpy, 
            bpy::args("image"), 
            "returns a numpy array representation of the image (no copy is performed)",
            //bpy::return_value_policy<bpy::manage_new_object, bpy::with_custodian_and_ward_postcall<0, 1> >());
            bpy::with_custodian_and_ward_postcall<0, 1>());
  
  bpy::def("image_from_numpy",
           image_from_numpy, 
           bpy::args("array"), 
           "returns a new Yayi image with the same dimension, size, type and content as the provided array."
           " The values of the array are copied",
           bpy::return_value_policy<bpy::manage_new_object>());

}



#endif /* YAYI_IO_NUMPY_ENABLED__ */
