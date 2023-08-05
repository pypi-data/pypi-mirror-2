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
#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>
#include <boost/bind.hpp>
#include <boost/function.hpp>

template <class V, V* p>
struct getSEPredefined 
{
  static yayi::se::IStructuringElement const* get() 
  {
    static yayi::se::IStructuringElement const* const v = p;
    return v->Clone();
  }
};

#if 0
#if 0
template <void const* const p>
struct getSEPredefinedVoid
{
  BOOST_STATIC_ASSERT(p != 0);

  static yayi::se::IStructuringElement const* get() 
  {
    static yayi::se::IStructuringElement const* const v = p;
    return v->Clone();
  }
};
#endif



template <class T>
  yayi::se::IStructuringElement const* super_func(T& se) 
  {
    return se.Clone();
  }


//template <class V, V* p>
struct getSEPredefined2 {
  yayi::se::IStructuringElement const* p;
  template <class V>
  getSEPredefined2(V* t) : p(t) {}

  yayi::se::IStructuringElement const* operator()() {
    //static yayi::se::IStructuringElement const* const v = p;
    return p->Clone();
  }
};

struct s_infer_type {
  template <class T> struct result {
    typedef T* type;
  };
  
  #if 0
  template <class T, T* p>
  struct result< p > {
    typedef T type;
  };
  #endif
  
  template <class T>
  T* operator()(T& p) {
    return &p;
  }
};


#define YAYI_SE_EXPORT_M(x)






template <yayi::se::IStructuringElement const* const *p>
yayi::se::IStructuringElement const* getPredefined2() {
  return *p;
}
#endif
typedef boost::function< yayi::se::IStructuringElement const* () > f_type;

struct s_bind {
  typedef yayi::se::IStructuringElement const* result_type;
  template <class T>
  yayi::se::IStructuringElement const* operator()(T& se) const
  {
    return se.Clone();
  }
};

void declare_predefined() 
{
  using namespace yayi;
  using namespace yayi::se;
  
  bpy::def("SESquare2D",    &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESquare2D >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SECross2D",     &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SECross2D  >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SEHex2D",       &(getSEPredefined<const s_neighborlist_se_hexa_x< s_coordinate<2> >,  &yayi::se::SEHex2D    >::get), bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESquare3D",    &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESquare3D >::get), bpy::return_value_policy<bpy::manage_new_object>());

  bpy::def("SESegmentX2D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESegmentX2D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentY2D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<2> >,         &yayi::se::SESegmentY2D>::get),bpy::return_value_policy<bpy::manage_new_object>());


  bpy::def("SESegmentX3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentX3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentY3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentY3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("SESegmentZ3D",  &(getSEPredefined<const s_neighborlist_se< s_coordinate<3> >,         &yayi::se::SESegmentZ3D>::get),bpy::return_value_policy<bpy::manage_new_object>());
  
  
  #if 0
  boost::bind(s_bind(), yayi::se::SEHex2D)();
  
  //static f_type se_hex = boost::bind(s_bind(), yayi::se::SEHex2D);
  static const f_type se_hex = boost::bind(s_bind(), yayi::se::SEHex2D);

  bpy::def(
    "SEHex2D",
    &se_hex,//getSEPredefinedVoid<((void*)&yayi::se::SEHex2D)>::get,//&boost::bind(s_bind(), yayi::se::SEHex2D)::operator(),
    bpy::return_value_policy<bpy::manage_new_object>());
  #endif
  
  /*s_infer_type o;
  o(yayi::se::SEHex2D);
  typedef s_infer_type::result< o(yayi::se::SEHex2D) >::type toto;
  */
  //bpy::scope().attr("SESquare2D") = (const yayi::se::IStructuringElement* const)&yayi::se::SESquare2D;
  //bpy::scope().attr("SEHex2D") = (const yayi::se::IStructuringElement* const)&yayi::se::SEHex2D;


}

