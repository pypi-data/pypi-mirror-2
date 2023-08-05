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
#include <Yayi/core/yayiCommon/common_variant.hpp>

using namespace yayi;
struct custom_variant_to_python
{

  static PyObject* from_variant_to_python(yayi::variant const& s) {
    
    using yayi::type;

    if(s.element_type.c_type == type::c_scalar) {
      switch(s.element_type.s_type) {
      case type::s_ui8: 
      case type::s_ui16: 
      case type::s_ui32: 
        return PyLong_FromUnsignedLong(static_cast<yaUINT32>(s));
        
      case type::s_ui64: 
        return PyLong_FromUnsignedLongLong(static_cast<yaUINT64>(s));
      
      case type::s_i8: 
      case type::s_i16: 
      case type::s_i32:
        return PyLong_FromLong(static_cast<yaINT32>(s));
      
      case type::s_i64:
        return PyLong_FromLongLong(static_cast<yaINT64>(s));
        
      case type::s_float: 
        return PyFloat_FromDouble(static_cast<yaF_simple>(s));
        
      case type::s_double:
        return PyFloat_FromDouble(static_cast<yaF_double>(s));
      
      case type::s_bool:
      {
        if(variant_field_from_type<yaBool>(s))
          Py_RETURN_TRUE;
        Py_RETURN_FALSE;
      }
        
      case type::s_string:
        return PyString_FromString(variant_field_from_type<string_type>(s).c_str());
      
      case type::s_wstring:
      {
        const wide_string_type& str_ = variant_field_from_type<wide_string_type>(s);
        return PyUnicode_FromWideChar(str_.c_str(), str_.size());
      }
        
      default:
        YAYI_THROW("Unsupported scalar type");
      }
    
    }
    else if(s.element_type.c_type == type::c_vector) {
      
      const std::vector<s_any_type>& vect = variant_field_from_type< std::vector<s_any_type> >(s);
      PyObject* out_t = PyTuple_New(vect.size());
      if(out_t == NULL)
        return 0;
      
      std::vector<s_any_type>::size_type i = 0, j = vect.size();
      for(; i < j; i++) {
        PyObject *p = 0;
        try {
          p = from_variant_to_python(vect[i]);
        } catch(yayi::errors::yaException &/*e*/) {
          Py_XDECREF(p);
          Py_DECREF(out_t);
          return 0;          
        }

        if(p == 0 || PyTuple_SetItem(out_t, i, p) != 0) {
          // Raffi : pas besoin de decref p: soit il n'existe pas, soit il appartient au tuple
          Py_DECREF(out_t);
          return 0;
        }
        //Py_DECREF(p);

      }
      return out_t;
    }
    
    else if(s.element_type.c_type == type::c_complex) 
    {
      if(s.element_type.s_type == type::s_float)
      {
        const std::complex<yaF_simple>& c = variant_field_from_type< std::complex<yaF_simple> >(s);
        PyObject* out_t = PyComplex_FromDoubles(static_cast<double>(std::real(c)), static_cast<double>(std::imag(c)));
        if(out_t == NULL)
          return 0;
        return out_t;
      }
      assert(s.element_type.s_type == type::s_double);
      const std::complex<yaF_double>& c = variant_field_from_type< std::complex<yaF_double> >(s);
      PyObject* out_t = PyComplex_FromDoubles(std::real(c), std::imag(c));
      if(out_t == NULL)
        return 0;
      return out_t;
    }
    else if(s.element_type.c_type == type::c_3) 
    {
      PyObject* out_t = PyTuple_New(3);
      if(out_t == NULL)
        return 0;
      
      switch(s.element_type.s_type) {
      case type::s_ui8: 
      case type::s_ui16: 
      case type::s_ui32:
      {
        typedef s_compound_pixel_t<yaUINT32, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyLong_FromUnsignedLong(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyLong_FromUnsignedLong(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyLong_FromUnsignedLong(pix[2])) != 0) ) 
        {
          Py_DECREF(out_t);
          return 0;
        }
        return out_t;
      }
      
      case type::s_ui64: 
      {
        typedef s_compound_pixel_t<yaUINT64, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyLong_FromUnsignedLongLong(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyLong_FromUnsignedLongLong(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyLong_FromUnsignedLongLong(pix[2])) != 0) ) 
        {
            Py_DECREF(out_t);
            return 0;
        }
        return out_t;
      }
              
      case type::s_i8: 
      case type::s_i16: 
      case type::s_i32:
      {
        typedef s_compound_pixel_t<yaINT32, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyLong_FromLong(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyLong_FromLong(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyLong_FromLong(pix[2])) != 0) ) 
        {
            Py_DECREF(out_t);
            return 0;
        }
        return out_t;
      }
      
      case type::s_i64:
      {
        typedef s_compound_pixel_t<yaINT64, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyLong_FromLongLong(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyLong_FromLongLong(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyLong_FromLongLong(pix[2])) != 0) ) 
        {
            Py_DECREF(out_t);
            return 0;
        }
        return out_t;
      }
              
      case type::s_float: 
      {
        typedef s_compound_pixel_t<yaF_simple, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyFloat_FromDouble(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyFloat_FromDouble(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyFloat_FromDouble(pix[2])) != 0) ) 
        {
            Py_DECREF(out_t);
            return 0;
        }
        return out_t;
      }
        
      case type::s_double:
      {
        typedef s_compound_pixel_t<yaF_double, mpl::int_<3> > pix_t;
        pix_t pix = s.operator pix_t();
        if( (PyTuple_SetItem(out_t, 0, PyFloat_FromDouble(pix[0])) != 0) || 
            (PyTuple_SetItem(out_t, 1, PyFloat_FromDouble(pix[1])) != 0) ||
            (PyTuple_SetItem(out_t, 2, PyFloat_FromDouble(pix[2])) != 0) ) 
        {
            Py_DECREF(out_t);
            return 0;
        }
        return out_t;
      }
        
      default:
        YAYI_THROW("Unsupported scalar type");
      }
    }        
    
    YAYI_THROW("Unsupported compound type");
    
    
    return 0;
  }



  static PyObject* convert(yayi::variant const& s)
  {
    return from_variant_to_python(s);
  }
};


struct custom_variant_from_python
{
  custom_variant_from_python()
  {
    boost::python::converter::registry::push_back(
      &convertible,
      &construct,
      boost::python::type_id<yayi::variant>());
  }
  
  static yayi::variant* do_convert(PyObject* obj_ptr, void * pos)
  {
    //static const long int l_max = PyInt_GetMax();
    
    if(PyBool_Check(obj_ptr)) 
    {
      yaBool b = obj_ptr == Py_True;
      return (pos ? new (pos) variant(b): new variant(b));
    }
    else if(PyLong_CheckExact(obj_ptr))
    {
      yaINT32 l = PyLong_AsLong(obj_ptr);
      if(l == -1) {
        PyObject * po = PyErr_Occurred();
        if(po != NULL && PyErr_ExceptionMatches(PyExc_OverflowError)) {
          yaINT64 ll = PyLong_AsLongLong(obj_ptr);
          return (pos ? new (pos) variant(ll): new variant(ll));
        }
      }
      return (pos ? new (pos) variant(l): new variant(l));
    }
    else if(PyInt_CheckExact(obj_ptr)) 
    {
      yaINT32 l = PyInt_AsLong(obj_ptr);
      if(l == -1) {
        PyObject * po = PyErr_Occurred();
        if(po != NULL && PyErr_ExceptionMatches(PyExc_OverflowError)) {
          yaINT64 ll = PyLong_AsLongLong(obj_ptr);
          return (pos ? new (pos) variant(ll): new variant(ll));
        }
      }
      return (pos ? new (pos) variant(l): new variant(l));
    }
    else if(PyFloat_CheckExact(obj_ptr))
    { 
      yaF_double f = PyFloat_AsDouble(obj_ptr);
      return (pos ? new (pos) variant(f): new variant(f));
    }
    else if(PyString_CheckExact(obj_ptr))
    {
      yayi::string_type s = PyString_AsString(obj_ptr); // or PyString_AS_STRING
      return (pos ? new (pos) variant(s): new variant(s));
    }
    else if(PyComplex_CheckExact(obj_ptr))
    {
      std::complex<double> s(PyComplex_RealAsDouble(obj_ptr), PyComplex_ImagAsDouble(obj_ptr));
      return (pos ? new (pos) variant(s): new variant(s));
    }
    else if(PyUnicode_CheckExact(obj_ptr))
    {
      Py_ssize_t size = PyUnicode_GET_SIZE(obj_ptr);
      wchar_t *temp = new wchar_t[size+1];
      Py_ssize_t ss = PyUnicode_AsWideChar((PyUnicodeObject*)obj_ptr, temp, size);
      if(ss == -1)
      {
        delete [] temp;
        return 0;
      }
      temp[size] = 0;
      yayi::wide_string_type s = temp;
      delete [] temp;
      return (pos ? new (pos) variant(s): new variant(s));
    }
    else if(PyTuple_CheckExact(obj_ptr))
    {
      std::vector<variant> v;
      for(Py_ssize_t i = 0, j = PyTuple_Size(obj_ptr); i < j; i++)
      {
        PyObject *py = PyTuple_GetItem(obj_ptr, i);
        variant *p = do_convert(py, 0);
        if(!p)
        {
          std::cout << "unable to convert element " << i << " of the tuple into a variant" << std::endl;
          return 0;
        }
        v.push_back(*p); // do better here, because 2 copies
        delete p;
        
      }
      return (pos ? new (pos) variant(v): new variant(v));
    }
    else if(PyList_CheckExact(obj_ptr))
    {
      std::vector<variant> v;
      for(Py_ssize_t i = 0, j = PyList_Size(obj_ptr); i < j; i++)
      {
        PyObject *py = PyList_GetItem(obj_ptr, i);
        variant *p = do_convert(py, 0);
        if(!p)
        {
          std::cout << "unable to convert element " << i << " of the list into a variant" << std::endl;
          return 0;
        }
        v.push_back(*p); // do better here, because 2 copies
        delete p;
        
      }
      return (pos ? new (pos) variant(v): new variant(v));
    }
    else if(PyDict_CheckExact(obj_ptr))
    {
      PyObject *key = 0, *value = 0;
      Py_ssize_t position = 0;
      std::vector<variant> v;

      while (PyDict_Next(obj_ptr, &position, &key, &value))
      {
        std::vector<variant> v_pair;        
        variant *p = do_convert(key, 0);
        if(!p)
        {
          std::cout << "unable to convert key for element " << position << " of the dictionnary into a variant" << std::endl;
          return 0;
        }
        
        v_pair.push_back(*p); // do better here, because 2 copies
        delete p;


        variant *p_v = do_convert(value, 0);
        if(!p)
        {
          std::cout << "unable to convert value element " << position << " of the dictionnary into a variant" << std::endl;
          return 0;
        }
        
        v_pair.push_back(*p_v); // do better here, because 2 copies
        delete p_v;
        
        v.push_back(v_pair);
      }
      
      return (pos ? new (pos) variant(v): new variant(v));      

    }
    
    return 0;
  }

  
  
  

  static void* convertible(PyObject* obj_ptr)
  {
    if(obj_ptr == 0)
      return 0;
    //if (!PyString_Check(obj_ptr)) return 0;
    else if(PyBool_Check(obj_ptr))
      return obj_ptr;
      
    else if(PyLong_CheckExact(obj_ptr))
      return obj_ptr;
      
    else if(PyInt_CheckExact(obj_ptr))
      return obj_ptr;
    
    else if(PyFloat_CheckExact(obj_ptr))// / PyFloat_AsDouble() / PyFloat_AsDOUBLE() 
      return obj_ptr;
    
    else if(PyString_CheckExact(obj_ptr))// / PyString_Check() / PyString_AsString() 
      return obj_ptr;
    
    else if(PyUnicode_CheckExact(obj_ptr))// / Py_UNICODE* PyUnicode_AS_UNICODE(PyObject *o) 
      return obj_ptr;
    
    else if(PyTuple_CheckExact(obj_ptr))
    {
      for(Py_ssize_t i = 0, j = PyTuple_Size(obj_ptr); i < j; i++)
      {
        if(convertible(PyTuple_GetItem(obj_ptr, i)) == 0)
          return 0;
      }
      return obj_ptr;
    }
    
    else if(PyList_CheckExact(obj_ptr))
    {
      for(Py_ssize_t i = 0, j = PyList_Size(obj_ptr); i < j; i++)
      {
        if(convertible(PyList_GetItem(obj_ptr, i)) == 0)
          return 0;
      }
      return obj_ptr;
    }
    
    else if(PyDict_CheckExact(obj_ptr))
    {
      PyObject *key = 0, *value = 0;
      Py_ssize_t pos = 0;

      while (PyDict_Next(obj_ptr, &pos, &key, &value)) {
        if(convertible(key) == 0)
          return 0;
        if(convertible(value) == 0)
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
    void* storage = ((boost::python::converter::rvalue_from_python_storage<yayi::variant>*)data)->storage.bytes;
    variant *var = do_convert(obj_ptr, storage);
    if (var == 0) boost::python::throw_error_already_set();
    data->convertible = storage;
  }
};


void declare_variants()
{
  boost::python::to_python_converter<yayi::variant, custom_variant_to_python>();
  custom_variant_from_python();
}





