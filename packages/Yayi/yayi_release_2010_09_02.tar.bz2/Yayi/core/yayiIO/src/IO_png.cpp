/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include "yayi_IO.hpp"
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>


#include <cstdio>
#include <algorithm>
#include <png.h>


namespace yayi {

  namespace IO {
  
    template <class image_t>
    bool png_read_helper(IImage* image, png_structp& png_ptr) {
        
      image_t* im = dynamic_cast<image_t*>(image);
      if(im == 0)
        return false;
    
      const typename image_t::coordinate_type::scalar_coordinate_type w = im->Size()[0], h = im->Size()[1];
      
      int number_passes = png_set_interlace_handling(png_ptr);
      const int number_of_rows = 7;
      png_bytep row_pointer[number_of_rows];
      for (int pass = 0; pass < number_passes; pass++)
      {
        for (int y = 0; y < h; y += number_of_rows)
        {
          int current_nb_row = std::min(number_of_rows, (int)(h-y));
          DEBUG_ASSERT(current_nb_row > 0, "Something wrong there : verify !");
          for(int k = 0; k < current_nb_row; k++) row_pointer[k] = (png_bytep)(&im->pixel((k+y) * w));
          png_read_rows(png_ptr, &row_pointer[0], png_bytepp_NULL, current_nb_row);
        }
      }
      return true;
    }
  
  
    const unsigned int PNG_BYTES_TO_CHECK = 4;
    
  
    yaRC readPNG (const string_type &filename, IImage* & image) {
 
      if(image != 0)
        return yaRC_E_null_pointer;

      FILE * infile = fopen(filename.c_str(), "rb");
      if(infile == 0)
      {
        return yaRC_E_file_io_error;
      }
      
      

      png_byte header[PNG_BYTES_TO_CHECK];      
      if(fread(header, 1, PNG_BYTES_TO_CHECK, infile) != PNG_BYTES_TO_CHECK) {
        fclose(infile);
        return yaRC_E_file_io_error;
      }


      bool is_png = png_sig_cmp(header, 0, PNG_BYTES_TO_CHECK) == 0;
      if (!is_png)
      {
        fclose(infile);
        return yaRC_E_file_io_error;
      }
      


      png_structp png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, png_voidp_NULL/*(png_voidp)&image*/, png_error_ptr_NULL, png_error_ptr_NULL);
      if (!png_ptr) {
        fclose(infile);
        return yaRC_E_unknown;
      }
      
      png_infop info_ptr = png_create_info_struct(png_ptr);
      if (!info_ptr)
      {
        png_destroy_read_struct(&png_ptr, (png_infopp)NULL, (png_infopp)NULL);
        fclose(infile);
        return yaRC_E_unknown;
      }

      png_infop end_info = png_create_info_struct(png_ptr);
      if (!end_info)
      {
        png_destroy_read_struct(&png_ptr, &info_ptr,(png_infopp)NULL);
        fclose(infile);
        return yaRC_E_unknown;
      }

      
      if (setjmp(png_jmpbuf(png_ptr)))
      {
        png_destroy_read_struct(&png_ptr, &info_ptr, &end_info);
        fclose(infile);
        if(image != 0)
          delete image;
        return yaRC_E_unknown;
      }


      png_init_io(png_ptr, infile);
      png_set_sig_bytes(png_ptr, PNG_BYTES_TO_CHECK);

      png_read_info(png_ptr, info_ptr);
      
      unsigned int width            = png_get_image_width(png_ptr, info_ptr);
      unsigned int height           = png_get_image_height(png_ptr, info_ptr);
      unsigned int bit_depth        = png_get_bit_depth(png_ptr, info_ptr);
      unsigned int color_type       = png_get_color_type(png_ptr, info_ptr);
      //unsigned int filter_method    = png_get_filter_type(png_ptr, info_ptr);
      unsigned int channels         = png_get_channels(png_ptr, info_ptr);

      // determiner type
      type im_type;
      if(color_type == PNG_COLOR_TYPE_GRAY) {
        im_type.c_type = type::c_scalar;
        im_type.s_type = bit_depth == 16 ? type::s_ui16 : type::s_ui8;
        if(bit_depth < 8) 
          png_set_expand_gray_1_2_4_to_8(png_ptr);
      }
      else if(channels == 3 || color_type == PNG_COLOR_TYPE_PALETTE) {
        im_type.c_type = type::c_3;
        im_type.s_type = bit_depth == 16 ? type::s_ui16 : type::s_ui8;
        if(color_type == PNG_COLOR_TYPE_PALETTE)
          png_set_palette_to_rgb(png_ptr);
      }
      else if(channels == 4)
      {
        im_type.c_type = type::c_4;
        im_type.s_type = bit_depth == 16 ? type::s_ui16 : type::s_ui8;      
      }
      else
      {
        DEBUG_INFO("Invalid value for the number of components : channels = " << (int)channels << " != (1 or 3 or 4)");
        fclose(infile);
        png_destroy_read_struct(&png_ptr, &info_ptr, png_infopp_NULL);
        return yaRC_E_unknown;        
      }
      
      if(im_type.s_type == type::s_ui16 && !yayi::is_big_endian)
      {
        png_set_swap(png_ptr);
      }      

      
      image = IImage::Create(im_type, 2);
      if(image == 0) {
        fclose(infile);
        png_destroy_read_struct(&png_ptr, &info_ptr, png_infopp_NULL);
        DEBUG_INFO("Cannot create the image of type " << im_type);
        return yaRC_E_unknown;
      }
      
      IImage::coordinate_type im_coords;// = image->GetSize();
      im_coords.set_dimension(2);
      im_coords[0] = width;
      im_coords[1] = height;

      if(image->SetSize(im_coords) != yaRC_ok) {
        fclose(infile);
        png_destroy_read_struct(&png_ptr, &info_ptr, png_infopp_NULL);
        delete image; image = 0;
        return yaRC_E_bad_size;
      }

      if(image->AllocateImage() != yaRC_ok) {
        fclose(infile);
        png_destroy_read_struct(&png_ptr, &info_ptr, png_infopp_NULL);
        delete image; image = 0;
        return yaRC_E_memory;
      }


      bool b_convert_ok = false;
      if(im_type.c_type == type::c_scalar) {
        if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_read_helper< Image<yaUINT8> >(image, png_ptr);
        }
        else {
          b_convert_ok = png_read_helper< Image<yaUINT16> >(image, png_ptr);
        }
      }
      else if(im_type.c_type == type::c_3) {
        if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_read_helper< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > >(image, png_ptr);
        }
        else {
          b_convert_ok = png_read_helper< Image<s_compound_pixel_t<yaUINT16, mpl::int_<3> > > >(image, png_ptr);
        }      
      }
      else {
       if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_read_helper< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > > >(image, png_ptr);
        }
        else {
          b_convert_ok = png_read_helper< Image<s_compound_pixel_t<yaUINT16, mpl::int_<4> > > >(image, png_ptr);
        }      
      }


      
      
      png_read_end(png_ptr, info_ptr);
      png_destroy_read_struct(&png_ptr, &info_ptr, &end_info);
      fclose(infile);

      return b_convert_ok ? yaRC_ok : yaRC_E_unknown;
      
    }
    
    
    template <class image_t>
    bool png_write_helper(const IImage* image, png_structp& png_ptr) {
      
      const image_t* im = dynamic_cast<const image_t*>(image);
      if(im == 0)
        return false;
      const typename image_t::coordinate_type::scalar_coordinate_type w = im->Size()[0], h = im->Size()[1];
      
      int number_passes = png_set_interlace_handling(png_ptr);
      const int number_of_rows = 7;
      png_bytep row_pointer[number_of_rows];
      
      for (int pass = 0; pass < number_passes; pass++)
      {
        for (int y = 0; y < h; y += number_of_rows)
        {
          int current_nb_row = std::min(number_of_rows, (int)(h-y));
          DEBUG_ASSERT(current_nb_row > 0, "Something wrong there : verify !");
          for(int k = 0; k < current_nb_row; k++) row_pointer[k] = (png_bytep)(&im->pixel((k+y) * w));
          png_write_rows(png_ptr, &row_pointer[0], current_nb_row); 
        }
      }
      return true;
    }
    
    yaRC writePNG(const string_type &filename, const IImage* const & image) {
      
      if(image == 0)
        return yaRC_E_null_pointer; 

      IImage::coordinate_type im_coords = image->GetSize();
      if(im_coords.dimension() < 2)
        return yaRC_E_bad_size;
        
      for(unsigned int i = 2; i < im_coords.dimension(); i ++) {
        if(im_coords[i] > 0)
          return yaRC_E_bad_size;
      }
      
      type im_type = image->DynamicType();
      if(im_type.c_type != type::c_scalar && im_type.c_type != type::c_3 && im_type.c_type != type::c_4)
        return yaRC_E_bad_colour;
      if(im_type.s_type != type::s_ui8 && im_type.s_type != type::s_ui16)
        return yaRC_E_bad_colour;
    
      FILE * outfile = fopen(filename.c_str(), "wb");
      if(outfile == 0)
      {
        return yaRC_E_file_io_error;
      }
      
      png_structp png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, png_voidp_NULL/*(png_voidp)&image*/, png_error_ptr_NULL, png_error_ptr_NULL);
      if (png_ptr == NULL)
      {
        fclose(outfile);
        return yaRC_E_unknown;
      }
      
      png_infop info_ptr = png_create_info_struct(png_ptr);
      if (info_ptr == NULL)
      {
        fclose(outfile);
        png_destroy_write_struct(&png_ptr,  png_infopp_NULL);
        return yaRC_E_unknown;
      }
      
      if (setjmp(png_jmpbuf(png_ptr)))
      {
        fclose(outfile);
        png_destroy_write_struct(&png_ptr, &info_ptr);
        return yaRC_E_unknown;
      }
      
      png_init_io(png_ptr, outfile);

      // init from image type
      int color_space = PNG_COLOR_TYPE_GRAY;
      if(im_type.c_type != type::c_scalar) {
        color_space = im_type.c_type == type::c_3 ? PNG_COLOR_TYPE_RGB : PNG_COLOR_TYPE_RGB_ALPHA;
      }
      
      png_set_IHDR(png_ptr, 
        info_ptr, 
        im_coords[0], 
        im_coords[1], 
        (im_type.s_type == type::s_ui8 ? 8:16), 
        color_space, 
        PNG_INTERLACE_ADAM7, 
        PNG_COMPRESSION_TYPE_BASE, 
        PNG_FILTER_TYPE_BASE);
      
      // some blablabla
      png_text text_ptr[1];
      text_ptr[0].key   = "Creator";
      text_ptr[0].text  = "Yayi";
      text_ptr[0].compression = PNG_TEXT_COMPRESSION_NONE;
      
      png_set_text(png_ptr, info_ptr, text_ptr, 1);
      png_write_info(png_ptr, info_ptr);
    
      if(im_type.s_type == type::s_ui16 && !yayi::is_big_endian)
      {
        png_set_swap(png_ptr);
      }      
      
      bool b_convert_ok = false;
      if(im_type.c_type == type::c_scalar) {      
        if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_write_helper< Image<yaUINT8> >(image, png_ptr);
        }
        else {
          b_convert_ok = png_write_helper< Image<yaUINT16> >(image, png_ptr);
        }
        
      }
      else if(im_type.c_type == type::c_3) {
        if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_write_helper< Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > >(image, png_ptr);
        }
        else {
          b_convert_ok = png_write_helper< Image<s_compound_pixel_t<yaUINT16, mpl::int_<3> > > >(image, png_ptr);
        }
      }
      else {
        // Swap location of alpha bytes from ARGB to RGBA
        // Raffi : on pourrait avoir besoin de cette fonction
        png_set_swap_alpha(png_ptr);
        if(im_type.s_type == type::s_ui8) {
          b_convert_ok = png_write_helper< Image<s_compound_pixel_t<yaUINT8, mpl::int_<4> > > >(image, png_ptr);
        }
        else {
          b_convert_ok = png_write_helper< Image<s_compound_pixel_t<yaUINT16, mpl::int_<4> > > >(image, png_ptr);
        }
      }

      
      png_write_end(png_ptr, info_ptr);
      png_destroy_write_struct(&png_ptr, &info_ptr);
      fclose(outfile);
      
      return b_convert_ok ? yaRC_ok : yaRC_E_unknown;

    }
    
  }

}

