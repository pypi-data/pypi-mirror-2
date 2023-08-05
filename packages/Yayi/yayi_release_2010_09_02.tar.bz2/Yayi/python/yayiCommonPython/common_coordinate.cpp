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
#include <Yayi/core/yayiCommon/common_coordinates.hpp>
#include <Yayi/core/yayiCommon/common_coordinates_operations_t.hpp>
#include <Yayi/core/yayiCommon/common_hyperrectangle.hpp>

#include <Yayi/core/yayiCommon/common_variant.hpp>

#include <iostream>

#include <boost/python/operators.hpp>
#include <boost/python/copy_const_reference.hpp>
#include <boost/python/return_by_value.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/stl_iterator.hpp>



struct custom_coordinate_to_python
{

  static PyObject* from_coordinate_to_python(yayi::s_coordinate<0> const& s) {
    using yayi::type;
    PyObject* out_t = PyTuple_New(s.dimension());
    if(out_t == NULL)
      return 0;

    unsigned int i = 0, j = s.dimension();
    for(; i < j; i++) {
      PyObject *p = 0;
      try {
        p = PyLong_FromLong(s[i]);
          
        if(p == NULL /*|| PyTuple_SET_ITEM(out_t, i, p) != 0*/) {
          Py_DECREF(out_t);
          return 0;
        }
        PyTuple_SET_ITEM(out_t, i, p);
        //Py_DECREF(p);
      } catch(yayi::errors::yaException &/*e*/) {
        Py_XDECREF(p);
        Py_DECREF(out_t);
        return 0;          
      }
    }
    return out_t;
  }    

  static PyObject* convert(yayi::s_coordinate<0> const& s)
  {
    return from_coordinate_to_python(s);
  }
};

struct custom_hyperrectangle_to_python
{

  static PyObject* from_hyperrectangle_to_python(yayi::s_hyper_rectangle<0> const& r) {
    using yayi::type;
    PyObject* out_t = PyTuple_New(2);
    if(out_t == NULL)
      return 0;

    PyObject *p1 = 0, *p2 = 0;
    try {
      p1 = custom_coordinate_to_python::from_coordinate_to_python(r.lowerleft_corner);
        
      if(p1 == NULL) {
        Py_DECREF(out_t);
        return 0;
      }
      PyTuple_SET_ITEM(out_t, 0, p1);
    } catch(yayi::errors::yaException &/*e*/) {
      Py_XDECREF(p1);
      Py_DECREF(out_t);
      return 0;          
    }

    try {
      p2 = custom_coordinate_to_python::from_coordinate_to_python(r.Size());
        
      if(p2 == NULL) {
        Py_DECREF(out_t);
        return 0;
      }
      PyTuple_SET_ITEM(out_t, 0, p2);
    } catch(yayi::errors::yaException &/*e*/) {
      Py_XDECREF(p2);
      Py_DECREF(out_t);
      return 0;          
    }
    return out_t;
  }    

  static PyObject* convert(yayi::s_hyper_rectangle<0> const& s)
  {
    return from_hyperrectangle_to_python(s);
  }
};


bool from_PyObjectToCoordinate(PyObject *p, yayi::s_coordinate<0>::scalar_coordinate_type& c)
{
  using namespace yayi;
  if(!PyLong_Check(p) && !PyInt_Check(p)) {
    return false;
  }

  yaINT32 l = PyLong_AsLong(p);
  if(l == -1) {
    PyObject * po = PyErr_Occurred();
    if(po != NULL)
    {
      if(PyErr_ExceptionMatches(PyExc_OverflowError)) {
        yaINT64 ll = PyLong_AsLongLong(p);
        if(ll > std::numeric_limits<yayi::s_coordinate<0>::scalar_coordinate_type>::max())
          return false;
        c = static_cast<yayi::s_coordinate<0>::scalar_coordinate_type>(ll);
        return true;
      }
      else 
        return false;
    }
  }
  c = l;
  return true;
}


struct custom_coordinate_from_python
{
  custom_coordinate_from_python()
  {
    boost::python::converter::registry::push_back(
      &convertible,
      &construct,
      boost::python::type_id< yayi::s_coordinate<0> >());
  }
  
  static bool make_convert_from_sequence(PyObject* obj_ptr, yayi::s_coordinate<0>& coord_out)
  {
    if(PyTuple_Check(obj_ptr))
    {
      int i = 0, j = PyTuple_Size(obj_ptr);
      coord_out.set_dimension(j);
      for(; i < j; i++)
      {
        PyObject *p = PyTuple_GetItem(obj_ptr, i);
        if(!from_PyObjectToCoordinate(p, coord_out[i]))
          return false;
      }
      return true;
    }
    else if(PyList_Check(obj_ptr))
    {
      int i = 0, j = PyList_Size(obj_ptr);
      coord_out.set_dimension(j);
      for(; i < j; i++)
      {
        PyObject *p = PyList_GetItem(obj_ptr, i);
        if(!from_PyObjectToCoordinate(p, coord_out[i]))
          return false;
      }
      return true;
    }
    return false;
  }
  
  static yayi::s_coordinate<0>* do_convert(PyObject* obj_ptr, void * pos)
  {
    using namespace yayi;
    //std::cout << "FROM PYTHON TO COORDINATE !!! (2)" << std::endl;
    yayi::s_coordinate<0>* s = new (pos) yayi::s_coordinate<0>();
    if(!make_convert_from_sequence(obj_ptr, *s))
    {
      s->~s_coordinate<0>();
      return 0;
    }
    return s;
  }

  
  
  

  static void* convertible(PyObject* obj_ptr)
  {
    //std::cout << "FROM PYTHON TO COORDINATE !!! convertible" << std::endl;  
    if(obj_ptr == 0)
      return 0;
    
    if(PyTuple_Check(obj_ptr))
    {
      //std::cout << "FROM PYTHON TO COORDINATE !!! convertible-tuple" << std::endl; 
      for(int i = 0, j = PyTuple_Size(obj_ptr); i < j; i++)
      {
        PyObject *p = PyTuple_GetItem(obj_ptr, i);
        if(!PyLong_Check(p) && !PyInt_Check(p)) {
         //     std::cout << "convertible : not 1" << std::endl; 
          return 0;
        }
      }
      return obj_ptr;
    }
    else if(PyList_Check(obj_ptr))
    {
      //std::cout << "FROM PYTHON TO COORDINATE !!! convertible-list" << std::endl; 
      for(int i = 0, j = PyList_Size(obj_ptr); i < j; i++)
      {
        PyObject *p = PyList_GetItem(obj_ptr, i);
        if(!PyLong_Check(p) && !PyInt_Check(p))
          return 0;
      }
      return obj_ptr;
    }
    
    return 0;
  }

  static void construct(
    PyObject* obj_ptr,
    boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    //std::cout << "FROM PYTHON TO COORDINATE !!! 0" << std::endl;  
    void* storage = ((boost::python::converter::rvalue_from_python_storage< yayi::s_coordinate<0> >*)data)->storage.bytes;
    yayi::s_coordinate<0> *var = do_convert(obj_ptr, storage);
    if (var == 0) boost::python::throw_error_already_set();
    data->convertible = storage;
  }
};


struct custom_hyperrectangle_from_python
{
  custom_hyperrectangle_from_python()
  {
    boost::python::converter::registry::push_back(
      &convertible,
      &construct,
      boost::python::type_id< yayi::s_hyper_rectangle<0> >());
  }
  
  static yayi::s_hyper_rectangle<0>* do_convert(PyObject* obj_ptr, void * pos)
  {
    using namespace yayi;
    

    if(PyTuple_Check(obj_ptr))
    {
      int j = PyTuple_Size(obj_ptr);
      if(j != 2)
        return 0;
      
      PyObject *p1 = PyTuple_GetItem(obj_ptr, 0);
      yayi::s_coordinate<0> c_temp_origin;
      if(!custom_coordinate_from_python::make_convert_from_sequence(p1,c_temp_origin))
      {
        return 0;
      }
      
      p1 = PyTuple_GetItem(obj_ptr, 1);
      yayi::s_coordinate<0> c_temp;
      if(!custom_coordinate_from_python::make_convert_from_sequence(p1,c_temp))
      {
        return 0;
      }
      yayi::s_hyper_rectangle<0>* s = new (pos) yayi::s_hyper_rectangle<0>(c_temp_origin, c_temp);
      return s;
    }
    else if(PyList_Check(obj_ptr))
    {
      int j = PyList_Size(obj_ptr);
      if(j != 2)
        return 0;
      
      PyObject *p1 = PyList_GetItem(obj_ptr, 0);
      yayi::s_coordinate<0> c_temp_origin;
      if(!custom_coordinate_from_python::make_convert_from_sequence(p1, c_temp_origin))
      {
        return 0;
      }
      
      p1 = PyList_GetItem(obj_ptr, 1);
      yayi::s_coordinate<0> c_temp;
      if(!custom_coordinate_from_python::make_convert_from_sequence(p1, c_temp))
      {
        return 0;
      }
      yayi::s_hyper_rectangle<0>* s = new (pos) yayi::s_hyper_rectangle<0>(c_temp_origin, c_temp);
      return s;
    }
    
    return 0;
  }

  
  
  

  static void* convertible(PyObject* obj_ptr)
  {
    //std::cout << "FROM PYTHON TO COORDINATE !!! convertible" << std::endl;  
    if(obj_ptr == 0)
      return 0;
    
    if(PyTuple_Check(obj_ptr))
    {
      int j = PyTuple_Size(obj_ptr);
      if(j != 2)
        return 0;
      for(int i = 0; i < j; i++)
      {
        PyObject *p = PyTuple_GetItem(obj_ptr, i);
        if(custom_coordinate_from_python::convertible(p) == 0)
          return 0;
      }
      return obj_ptr;
    }
    else if(PyList_Check(obj_ptr))
    {
      //std::cout << "FROM PYTHON TO COORDINATE !!! convertible-list" << std::endl; 
      int j = PyList_Size(obj_ptr);
      if(j != 2)
        return 0;
      for(int i = 0; i < j; i++)
      {
        PyObject *p = PyList_GetItem(obj_ptr, i);
        if(custom_coordinate_from_python::convertible(p) == 0)
          return 0;
      }
      return obj_ptr;
    }
    
    return 0;
  }

  static void construct(
    PyObject* obj_ptr,
    boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    //std::cout << "FROM PYTHON TO COORDINATE !!! 0" << std::endl;  
    void* storage = ((boost::python::converter::rvalue_from_python_storage< yayi::s_hyper_rectangle<0> >*)data)->storage.bytes;
    yayi::s_hyper_rectangle<0> *var = do_convert(obj_ptr, storage);
    if (var == 0) boost::python::throw_error_already_set();
    data->convertible = storage;
  }
};



std::string hyperrectangle_string(yayi::s_hyper_rectangle<0> const& h)
{
  std::ostringstream s;
  s << h.lowerleft_corner << " " << h.Size();
  return s.str();
}


bool are_set_of_points_equal_wrapper(bpy::object const& o1, bpy::object const& o2)
{
  bpy::stl_input_iterator< yayi::s_coordinate<0> > begin(o1), end, begin2(o2), end2;
  return yayi::are_sets_of_points_equal(std::list< yayi::s_coordinate<0> >(begin, end), std::list< yayi::s_coordinate<0> >(begin2, end2));
}

void declare_coordinate()
{
  boost::python::to_python_converter<yayi::s_coordinate<0>, custom_coordinate_to_python>();
  custom_coordinate_from_python();

  //boost::python::to_python_converter<yayi::s_hyper_rectangle<0>, custom_hyperrectangle_to_python>();
  custom_hyperrectangle_from_python();

  bpy::class_< yayi::s_hyper_rectangle<0> >("HyperRectangle", "A generic rectangle structure in any dimension (lower bound and upper bound)")
    .def(bpy::init<>())
    .def(bpy::init< yayi::s_hyper_rectangle<0> >("Construct a copy of the provided hyperrectangle"))
    .def(bpy::init< yayi::s_coordinate<0>, yayi::s_coordinate<0> >(bpy::args("origin", "size"), "Construct an hyperrectangle from an origin and a size"))
    .def("IsInside",  &yayi::s_hyper_rectangle<0>::is_inside, "tests if the provided point is inside the hyperrectangle")
    .add_property("Size",     &yayi::s_hyper_rectangle<0>::Size, &yayi::s_hyper_rectangle<0>::SetSize)
    .def("GetSize",           &yayi::s_hyper_rectangle<0>::Size,      "returns the size of the hyperrectangle")
    .def("SetSize",           &yayi::s_hyper_rectangle<0>::SetSize,   "sets the size of the hyperrectangle")
    .def(bpy::self == bpy::self)
    .add_property("Origin",
      bpy::make_getter(&yayi::s_hyper_rectangle<0>::lowerleft_corner, bpy::return_value_policy<bpy::return_by_value>()), 
      &yayi::s_hyper_rectangle<0>::SetOrigin)
    .add_property("upper_right", bpy::make_getter(&yayi::s_hyper_rectangle<0>::upperright_corner, bpy::return_value_policy<bpy::return_by_value>()))//boost::python::return_value_policy<boost::python::copy_const_reference>()))
    .def("__str__",  &hyperrectangle_string)
  ;
  bpy::implicitly_convertible< yayi::s_hyper_rectangle<0>, yayi::variant >();
  
  bpy::def("Transpose", 
    (yayi::s_coordinate<0> (*)(const yayi::s_coordinate<0> &))&yayi::transpose< yayi::scalar_coordinate >, 
    "Coordinate transposition");

  bpy::def("TransposeWithCenter", 
    (yayi::s_coordinate<0> (*)(const yayi::s_coordinate<0> &, const yayi::s_coordinate<0> &))&yayi::transpose< yayi::s_coordinate<0> >, 
    "Coordinate transposition");

  bpy::def("AreSetOfPointsEqual", 
    &are_set_of_points_equal_wrapper,
    bpy::args("set1", "set2"),
    "returns true if set1 and set2 contain the same points (with possible duplicate coordinates");
}
