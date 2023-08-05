/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiStructuringElement/yayiStructuringElement.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeNeighborhood_t.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>

#include <boost/mpl/lambda.hpp>
#include <iostream>

namespace yayi { namespace se {


  // This method is to be defined in case of additional structuring element support
  template <class im_type, class se_type> IConstNeighborhood* template_factory_helper_3(im_type& im, const IStructuringElement& ise) {
    //std::cout << __FUNCTION__ << std::endl;
    const se_type &se = dynamic_cast<const se_type&>(ise);
    return new s_runtime_neighborhood<im_type, se_type>(im, se);
  }


  template <class im_type, class im_interface> 
  IConstNeighborhood* template_factory_helper_2(im_interface& iim, const IStructuringElement& se) 
  {
    typedef typename mpl::if_<boost::is_const<im_interface>, typename add_const<im_type>::type, im_type >::type im_type_with_const_defined;
    im_type_with_const_defined &im = dynamic_cast<im_type_with_const_defined&>(iim);

    switch(se.GetSubType()) {
    case e_sest_neighborlist_generic_single:
      return template_factory_helper_3<const im_type, s_neighborlist_se<typename im_type_with_const_defined::coordinate_type> >(im, se);
    case e_sest_neighborlist_hexa:
      return template_factory_helper_3<const im_type, s_neighborlist_se_hexa_x<typename im_type_with_const_defined::coordinate_type> >(im, se);
    
    default:
      YAYI_THROW("Unsupported subtype structuring element");
      return 0;
    }
  }


  template <class compound_type_lambda_, int dimension, class im_interface> 
  IConstNeighborhood* template_factory_helper_1_type(im_interface& im, const IStructuringElement& se)
	{
    //std::cout << __FUNCTION__ << "   dimension  =  " << dimension << std::endl;
		switch(im.DynamicType().s_type)
		{
		case type::s_ui8:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaUINT8>::type, s_coordinate<dimension> > >(im, se);
		case type::s_i8:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaINT8>::type, s_coordinate<dimension> > >(im, se);
		case type::s_ui16:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaUINT16>::type, s_coordinate<dimension> > >(im, se);
		case type::s_i16:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaINT16>::type, s_coordinate<dimension> > >(im, se);
		case type::s_ui32:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaUINT32>::type, s_coordinate<dimension> > >(im, se);
		case type::s_i32:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaINT32>::type, s_coordinate<dimension> > >(im, se);
		case type::s_float:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaF_simple>::type, s_coordinate<dimension> > >(im, se);
		case type::s_double:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaF_double>::type, s_coordinate<dimension> > >(im, se);

		default:
			YAYI_THROW("Unsupported scalar type");
      return 0;
			
		}

    return 0;
  }

  template <class compound_type_lambda_, int dimension, class im_interface> 
  IConstNeighborhood* template_factory_helper_1_type_only_float_types(im_interface& im, const IStructuringElement& se)
  {
    //std::cout << __FUNCTION__ << std::endl;
		switch(im.DynamicType().s_type)
		{
		case type::s_float:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaF_simple>::type, s_coordinate<dimension> > >(im, se);
		case type::s_double:
      return template_factory_helper_2< Image<typename compound_type_lambda_::type::template apply<yaF_double>::type, s_coordinate<dimension> > >(im, se);
		default:
			YAYI_THROW("Unsupported scalar type");
      return 0;	
		}
    return 0;
  }


  template <int dim, class im_interface> 
  IConstNeighborhood* template_factory_helper_1(im_interface& im, const IStructuringElement& se)
  {
    //std::cout << __FUNCTION__ << std::endl;
    switch(im.DynamicType().c_type)
    {
    case type::c_scalar:
      return template_factory_helper_1_type<mpl::lambda< mpl::_1 >, dim>(im, se);
    case type::c_complex:
      return template_factory_helper_1_type_only_float_types<mpl::lambda< std::complex<mpl::_1> >, dim>(im, se);
    case type::c_3:
      //std::cout << "OK !!! " << std::endl;
      return template_factory_helper_1_type<mpl::lambda< s_compound_pixel_t<mpl::_1, mpl::int_<3> > >, dim>(im, se);
    case type::c_4:
      //std::cout << "4 NON OK !!! " << std::endl;
      return template_factory_helper_1_type<mpl::lambda< s_compound_pixel_t<mpl::_1, mpl::int_<4> > >, dim>(im, se);

    default:
      YAYI_THROW("Unsupported compound type");
      return 0;
    }
  }

  IConstNeighborhood* NeighborListCreate(const IImage& im, const IStructuringElement& se) {

    //std::cout << __FUNCTION__ << std::endl;
    switch(im.GetSize().dimension()) {
    case 2:
      return template_factory_helper_1<2>(im, se);
    case 3:
      return template_factory_helper_1<3>(im, se);
    case 4:
      return template_factory_helper_1<4>(im, se);
    
    default:
      YAYI_THROW("Unsupported dimension");
      return 0;
    }

  }


}}
