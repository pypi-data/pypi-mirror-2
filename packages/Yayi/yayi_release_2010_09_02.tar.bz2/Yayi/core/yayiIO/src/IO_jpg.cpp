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

extern "C" {
  // jpeg specific headers
  #include "jpeglib.h"
  #include <setjmp.h>
}

namespace yayi {

  namespace IO {
  
    template <class image_t>
    void jpg_read_helper(image_t& im, jpeg_decompress_struct& cinfo) {
      const typename image_t::coordinate_type::scalar_coordinate_type w = im.Size()[0];//, h = im.Size()[1];
      JSAMPROW row_pointer[1];
      while (cinfo.output_scanline < cinfo.output_height) {
        row_pointer[0] = (JSAMPROW)(&im.pixel(cinfo.output_scanline * w));
        jpeg_read_scanlines(&cinfo, row_pointer, 1); 
      }
     
    }
  
    struct my_error_mgr {
      struct jpeg_error_mgr pub;  /* "public" fields */
      jmp_buf setjmp_buffer;  /* for return to caller */
    };

    typedef struct my_error_mgr * my_error_ptr;
    
    METHODDEF(void) my_error_exit (j_common_ptr cinfo)
    {
      /* cinfo->err really points to a my_error_mgr struct, so coerce pointer */
      my_error_ptr myerr = (my_error_ptr) cinfo->err;

      /* Always display the message. */
      /* We could postpone this until after returning, if we chose. */
      (*cinfo->err->output_message) (cinfo);

      /* Return control to the setjmp point */
      longjmp(myerr->setjmp_buffer, 1);
    }
  
    yaRC readJPG (const string_type &filename, IImage* & image) {
 
      if(image != 0)
        return yaRC_E_null_pointer;
        
        
        
      FILE* infile = fopen(filename.c_str(), "rb");
      if(infile == 0)
      {
        return yaRC_E_file_io_error;
      }
      
      jpeg_decompress_struct cinfo;
      my_error_mgr jerr;

      // standard error handling in JPEG lib
      cinfo.err = jpeg_std_error(&jerr.pub);
      jerr.pub.error_exit = my_error_exit;
      
      /* Establish the setjmp return context for my_error_exit to use. */
      if (setjmp(jerr.setjmp_buffer)) 
      {
        /* If we get here, the JPEG code has signaled an error.
         * We need to clean up the JPEG object, close the input file, and return.
         */
        jpeg_destroy_decompress(&cinfo);
        fclose(infile);
        DEBUG_INFO("An unknown error occured in lib JPEG");
        return yaRC_E_unknown;
      }
      
      
      jpeg_create_decompress(&cinfo);

      jpeg_stdio_src(&cinfo, infile);
      jpeg_read_header(&cinfo, TRUE);
      
      // determiner type
      type im_type;
      if(cinfo.num_components == 1) {
        im_type.c_type = type::c_scalar;
        if(cinfo.jpeg_color_space != JCS_GRAYSCALE) {
          DEBUG_INFO("Something wrong with the color space : value = " << (int)cinfo.jpeg_color_space << " != JCS_GRAYSCALE = " << (int)JCS_GRAYSCALE);
          cinfo.out_color_space = JCS_GRAYSCALE;
        }
      }
      else if(cinfo.num_components == 3) {
        im_type.c_type = type::c_3;
        if(cinfo.jpeg_color_space == JCS_UNKNOWN){
          DEBUG_INFO("Color space unknown: setting the output to RGB");
          cinfo.out_color_space = JCS_UNKNOWN;/*JCS_RGB;*/
        }
        else if(cinfo.jpeg_color_space != JCS_RGB) {
          //DEBUG_INFO("Something wrong with the color space : value = " << (int)cinfo.jpeg_color_space << " != JCS_RGB = " << (int)JCS_RGB);
          cinfo.out_color_space = JCS_RGB;
        }
      }
      else 
      {
        DEBUG_INFO("Invalid value for the number of components : cinfo.num_components = " << (int)cinfo.num_components << " != (1 or 3)");
        fclose(infile);
        jpeg_destroy_decompress(&cinfo);
        return yaRC_E_unknown;        
      }

      im_type.s_type = type::s_ui8;
      
      image = IImage::Create(im_type, 2);
      if(image == 0) {
        fclose(infile);
        jpeg_destroy_decompress(&cinfo);
        DEBUG_INFO("Cannot create the image of type " << im_type);
        return yaRC_E_unknown;
      }
      
      IImage::coordinate_type im_coords;// = image->GetSize();
      im_coords.set_dimension(2);
      im_coords[0] = cinfo.image_width;
      im_coords[1] = cinfo.image_height;

      if(image->SetSize(im_coords) != yaRC_ok) {
        fclose(infile);
        jpeg_destroy_decompress(&cinfo);
        delete image; image = 0;
        return yaRC_E_bad_size;
      }

      if(image->AllocateImage() != yaRC_ok) {
        fclose(infile);
        jpeg_destroy_decompress(&cinfo);
        delete image; image = 0;
        return yaRC_E_memory;
      }

      
      jpeg_start_decompress(&cinfo);
      
      bool b_convert_ok = false;
      if(im_type.c_type == type::c_scalar) {
        typedef Image<yaUINT8> image_type;
        
        image_type* im = dynamic_cast<image_type*>(image);
        if(im != 0) {
          jpg_read_helper(*im, cinfo);
          b_convert_ok = true;
        }
      }
      else {
        typedef Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > image_type;
        
        image_type* im = dynamic_cast<image_type*>(image);
        if(im != 0) {
          jpg_read_helper(*im, cinfo);
          b_convert_ok = true;
        }      
      }

      jpeg_finish_decompress(&cinfo);
      fclose(infile);
      jpeg_destroy_decompress(&cinfo);
      
      return b_convert_ok ? yaRC_ok : yaRC_E_unknown;
    }
    
    
    
    
    template <class image_t>
    void jpg_write_helper(const image_t& im, jpeg_compress_struct& cinfo) {
      const typename image_t::coordinate_type::scalar_coordinate_type w = im.Size()[0];
      JSAMPROW row_pointer[1];
      while (cinfo.next_scanline < cinfo.image_height) {
        /* jpeg_write_scanlines expects an array of pointers to scanlines.
         * Here the array is only one element long, but you could pass
         * more than one scanline at a time if that's more convenient.
         */
        row_pointer[0] = (JSAMPROW)const_cast<typename image_t::pixel_type*>(&im.pixel(cinfo.next_scanline * w));
        (void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
      }
    }
    
    yaRC writeJPG(const string_type &filename, const IImage* const & image) {
      
      const int quality = 100;
    
    
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
      if(im_type.c_type != type::c_scalar && im_type.c_type != type::c_3)
        return yaRC_E_bad_colour;
      if(im_type.s_type != type::s_ui8)
        return yaRC_E_bad_colour;
    
      FILE * outfile = fopen(filename.c_str(), "wb");
      if(outfile == 0)
      {
        return yaRC_E_file_io_error;
      }
      
      jpeg_compress_struct cinfo;
      jpeg_error_mgr jerr;

      cinfo.err = jpeg_std_error(&jerr);
      jpeg_create_compress(&cinfo);
      jpeg_stdio_dest(&cinfo, outfile);
      
      
      // init from image type
      cinfo.image_width       = im_coords[0];
      cinfo.image_height      = im_coords[1];
      
      cinfo.input_components  = im_type.c_type != type::c_scalar ? 3 : 1;
      cinfo.in_color_space    = im_type.c_type != type::c_scalar ? /*JCS_UNKNOWN*/JCS_RGB : JCS_GRAYSCALE;
      jpeg_set_defaults(&cinfo);

      jpeg_set_colorspace(&cinfo, (im_type.c_type != type::c_scalar ? /*JCS_UNKNOWN*/JCS_RGB : JCS_GRAYSCALE));

      jpeg_set_quality(&cinfo, quality, TRUE /* limit to baseline-JPEG values */);
      
      jpeg_start_compress(&cinfo, TRUE);
      
      
      bool b_convert_ok = false;
      if(im_type.c_type == type::c_scalar) {
        typedef Image<yaUINT8> image_type;
        
        const image_type* im = dynamic_cast<const image_type*>(image);
        if(im != 0) {
          jpg_write_helper(*im, cinfo);
          b_convert_ok = true;
        }
        
      }
      else {
        typedef Image<s_compound_pixel_t<yaUINT8, mpl::int_<3> > > image_type;
        
        const image_type* im = dynamic_cast<const image_type*>(image);
        if(im != 0) {
          jpg_write_helper(*im, cinfo);
          b_convert_ok = true;
        }      
      }

      
      jpeg_finish_compress(&cinfo);
      fclose(outfile);
      jpeg_destroy_compress(&cinfo);
      
      return b_convert_ok ? yaRC_ok : yaRC_E_unknown;
    }
  
  
  }
}

