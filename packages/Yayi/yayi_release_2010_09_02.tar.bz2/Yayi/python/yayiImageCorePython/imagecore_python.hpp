/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef IMAGECORE_PYTHON_HPP__
#define IMAGECORE_PYTHON_HPP__

#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <boost/python/def.hpp>

#include <boost/weak_ptr.hpp>

namespace bpy = boost::python;

#include <Yayi/core/yayiCommon/common_types.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>


namespace yayi {

  //! Simple interface iterator wrapper
  template <class iterator_interface_>
  class IGenericWrapper : public IObject
  {
    typedef IGenericWrapper<iterator_interface_> this_type;
    
  protected:
    boost::shared_ptr<iterator_interface_> itc, itce, itcb;
    
  public:
    typedef iterator_interface_ iterator_interface;
    typedef typename iterator_interface::pixel_type pixel_type;
    
  public:
    virtual ~IGenericWrapper() {}
    IGenericWrapper(const this_type& r) : itc(r.itc), itce(r.itce), itcb(r.itcb) {}
    IGenericWrapper(iterator_interface* it_, iterator_interface* ite_) : itc(it_), itce(ite_), itcb(itc) {
      if(!it_ || !ite_)
        throw errors::yaException(yaRC_E_allocation);
    }

    // IObject
    virtual type DynamicType() const {
      return itc->DynamicType();
    }
    virtual string_type Description() const {
      return itc->Description();
    }
        
    this_type& operator++() {
      if(itc->is_equal(itce.get())) {
        PyErr_SetObject(PyExc_StopIteration, Py_None);
        boost::python::throw_error_already_set();
      }
    
      yaRC res = itc->next();
      if(res != yaRC_ok)
        YAYI_THROW(res);      

      return *this;    
    }
    
    this_type& operator--() {
      if(itc->is_equal(itcb.get())) {
        PyErr_SetObject(PyExc_StopIteration, Py_None);
        boost::python::throw_error_already_set();
      }
    
      yaRC res = itc->previous();
      if(res != yaRC_ok)
        YAYI_THROW(res);   //throw errors::yaException(res);      

      return *this;
    }
    

    pixel_type getPixel() const {
      if(itc->is_equal(itce.get())) {
        DEBUG_INFO("GetPixel : Deferencing after the end!");
        PyErr_SetString(PyExc_RuntimeError, "Deferencing after the end of the iteration");
        boost::python::throw_error_already_set();
      }
      return itc->getPixel();
    }
    
    virtual pixel_type next() {
      if(itc->is_equal(itce.get())) {
        PyErr_SetObject(PyExc_StopIteration, Py_None);
        boost::python::throw_error_already_set();
      }    
    
      pixel_type p = itc->getPixel();
      yaRC res = itc->next();
      if(res != yaRC_ok)
        YAYI_THROW(res); 
      return p;    
    }
    
    bool has_next() const 
    {
      return itc->is_different(itce.get());
    }
    
    virtual pixel_type previous() {
      if(itc->is_equal(itcb.get())) {
        PyErr_SetObject(PyExc_StopIteration, Py_None);
        boost::python::throw_error_already_set();
      }    
      pixel_type p = itc->getPixel();
      yaRC res = itc->previous();
      if(res != yaRC_ok)
        YAYI_THROW(res); 
      return p;
    }
    
    pixel_type operator*() const 
    {
      return itc->getPixel();
    }
  
    bool operator==(const this_type& r) const {
      return itc->is_equal(r.itc.get());
    }
    
    bool operator!=(const this_type& r) const {
      return itc->is_different(r.itc.get());
    }
    
    iterator_interface* ptr() {
      return itc.get();
    }
    iterator_interface const* ptr() const {
      return itc.get();
    }    
    
  };
  
  
  typedef IGenericWrapper<IConstIterator> IConstIteratorWrapper;

  
  class IIteratorWrapper : public IConstIteratorWrapper {
    typedef IIterator iterator_interface;
    iterator_interface* itc2;
    typedef IConstIteratorWrapper parent_type;
    
  public:

    IIteratorWrapper(const IIteratorWrapper& r) : parent_type(r), itc2(r.itc2) {}
  
    IIteratorWrapper(iterator_interface* itb, iterator_interface *ite) : 
      parent_type(dynamic_cast<IConstIterator*>(itb), dynamic_cast<IConstIterator*>(ite)), 
      itc2(itb) // same pointer as itb, so ok, itb advances, itc2 sets the good pixels
    {
      //itc2 = parent_type::itc;
    }
  
    yaRC setPixel(const pixel_type &p) {
      //std::cout << "offset " << itc->GetOffset() << " / " << itce.get()->GetOffset() << std::endl;
      if(itc->is_equal(itce.get())) {
        DEBUG_INFO("SetPixel : Deferencing after the end!");
        PyErr_SetString(PyExc_RuntimeError, "Deferencing after the end of the iteration");
        boost::python::throw_error_already_set();
      }
      YAYI_ASSERT(itc2->setPixel(p) == yaRC_ok, "erreur set pixel");
      return itc2->setPixel(p);
    }
    
    
  };

}


#endif /* IMAGECORE_PYTHON_HPP__ */
