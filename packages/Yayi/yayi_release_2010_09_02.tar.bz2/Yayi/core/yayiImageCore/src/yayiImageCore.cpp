/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>

#include <boost/mpl/lambda.hpp>
#include <iostream>


namespace yayi
{

  template <class compound_type_lambda_, int dimension>
  IImage* image_factory_outer_type_helper(const type& c)
	{
		switch(c.s_type)
		{
		case type::s_ui8:
      return new Image<typename compound_type_lambda_::type::template apply<yaUINT8>::type, s_coordinate<dimension> >();
		case type::s_i8:
      return new Image<typename compound_type_lambda_::type::template apply<yaINT8>::type, s_coordinate<dimension> >();
		case type::s_ui16:
      return new Image<typename compound_type_lambda_::type::template apply<yaUINT16>::type, s_coordinate<dimension> >();
		case type::s_i16:
      return new Image<typename compound_type_lambda_::type::template apply<yaINT16>::type, s_coordinate<dimension> >();
		case type::s_ui32:
      return new Image<typename compound_type_lambda_::type::template apply<yaUINT32>::type, s_coordinate<dimension> >();
		case type::s_i32:
      return new Image<typename compound_type_lambda_::type::template apply<yaINT32>::type, s_coordinate<dimension> >();
		case type::s_float:
      return new Image<typename compound_type_lambda_::type::template apply<yaF_simple>::type, s_coordinate<dimension> >();
		case type::s_double:
      return new Image<typename compound_type_lambda_::type::template apply<yaF_double>::type, s_coordinate<dimension> >();
		default:
			YAYI_THROW("Unsupported scalar type");
      return 0;
			
		}

    return 0;
  }

  template <class compound_type_lambda_, int dimension>
  IImage* image_factory_outer_type_helper_only_float_types(const type& c)
  {
		switch(c.s_type)
		{
		case type::s_float:
      return new Image<typename compound_type_lambda_::type::template apply<yaF_simple>::type, s_coordinate<dimension> >();
		case type::s_double:
      return new Image<typename compound_type_lambda_::type::template apply<yaF_double>::type, s_coordinate<dimension> >();
		default:
			YAYI_THROW("Unsupported scalar type");
      return 0;
			
		}

    return 0;
  }


  template <int dim>
  IImage* image_factory_helper_dimension(const type &c)
  {
    switch(c.c_type)
    {
    case type::c_scalar:
      return image_factory_outer_type_helper<mpl::lambda< mpl::_1 >, dim>(c);
    case type::c_complex:
      return image_factory_outer_type_helper_only_float_types<mpl::lambda< std::complex<mpl::_1> >, dim>(c);
    case type::c_3:
      return image_factory_outer_type_helper<mpl::lambda< s_compound_pixel_t<mpl::_1, mpl::int_<3> > >, dim>(c);
    case type::c_4:
      return image_factory_outer_type_helper<mpl::lambda< s_compound_pixel_t<mpl::_1, mpl::int_<4> > >, dim>(c);

    default:
        YAYI_THROW("Unsupported compound type");
        return 0;
    }
  }



	IImage* IImage::Create(type c, yaUINT8 dimension)
	{

    switch(dimension)
    {
      case 0:
      case 1:
        YAYI_THROW("Cannot create an image of dimension 0 or 1");
        return 0;
      
      case 2: return image_factory_helper_dimension<2>(c);
      case 3: return image_factory_helper_dimension<3>(c);
      case 4: return image_factory_helper_dimension<4>(c);
      default:
        YAYI_THROW("Unsupported dimension");
        return 0;
    }
	}


}

