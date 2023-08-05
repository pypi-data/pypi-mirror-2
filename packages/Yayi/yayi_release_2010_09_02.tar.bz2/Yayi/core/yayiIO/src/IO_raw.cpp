/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */




#include <Yayi/core/yayiIO/include/yayi_IO.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>
#include <fstream>

namespace yayi
{
  namespace IO
  {
  
    template <class pixel_t, int dim>
    yaRC readRAW_helper(std::ifstream &f, const s_coordinate<dim>& c, IImage*& imout) {
    
      Image<pixel_t, s_coordinate<dim> >* pim = dynamic_cast<Image<pixel_t, s_coordinate<dim> >*>(imout);
      if(pim == 0) {
        YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imout->Description());
        return yaRC_E_unknown;
      }
      
      offset size = total_number_of_points(c);
      
      f.read(reinterpret_cast<char *>(&pim->pixel(0)), sizeof(pixel_t) * size);
    
      return yaRC_ok;
    }

    template <class pixel_t>
    yaRC readRAW_helper_dim(std::ifstream &f, const s_coordinate<0>& c, IImage*& imout) {
      int dim = get_last_dimension(c);
      switch(dim) {
        case 2:
          return readRAW_helper<pixel_t>(f, s_coordinate<2>(c), imout);
        case 3:
          return readRAW_helper<pixel_t>(f, s_coordinate<3>(c), imout);
        case 4:
          return readRAW_helper<pixel_t>(f, s_coordinate<4>(c), imout);
          
        default:
          return yaRC_E_not_implemented;
      }
    }
  
    
    yaRC readRAW (const string_type &filename, const s_coordinate<0> &sizes, const type &image_type_, IImage* &out_image)
    {
    
      std::ifstream f(filename.c_str(), std::ios::binary);
      if(!f.is_open()) 
      {
        YAYI_DEBUG_MESSAGE("Unable to open file " + filename);
        return yaRC_E_file_io_error;
      }
      
      int dim = get_last_dimension(sizes);
      IImage *temp = IImage::Create(image_type_, dim);
      
      if(temp == 0)
        return yaRC_E_unknown;
      
      yaRC ret = temp->SetSize(sizes);
      if(ret != yaRC_ok)
        return ret;
      
      ret = temp->AllocateImage();
      if(ret != yaRC_ok)
        return ret;

      
      std::auto_ptr<IImage> lock(temp);
      

      
      switch(image_type_.c_type) {
      case type::c_scalar:
      {
        switch(image_type_.s_type) {
        case type::s_ui8:  ret = readRAW_helper_dim<yaUINT8> (f, sizes, temp); break;
        case type::s_ui16: ret = readRAW_helper_dim<yaUINT16>(f, sizes, temp); break;
        case type::s_ui32: ret = readRAW_helper_dim<yaUINT32>(f, sizes, temp); break;
        case type::s_ui64: ret = readRAW_helper_dim<yaUINT64>(f, sizes, temp); break;
          
        case type::s_i8:   ret = readRAW_helper_dim<yaINT8> (f, sizes, temp); break;
        case type::s_i16:  ret = readRAW_helper_dim<yaINT16>(f, sizes, temp); break;
        case type::s_i32:  ret = readRAW_helper_dim<yaINT32>(f, sizes, temp); break;
        case type::s_i64:  ret = readRAW_helper_dim<yaINT64>(f, sizes, temp); break;
        
        case type::s_float:   ret = readRAW_helper_dim<yaF_simple>(f, sizes, temp); break;
        case type::s_double:  ret = readRAW_helper_dim<yaF_double>(f, sizes, temp); break;
        default:
          return yaRC_E_not_implemented;
        }
        
        break;
        
      }
      
      default:
        //delete temp;
        return yaRC_E_not_implemented;
      }
      
      if(ret != yaRC_ok)
        return ret;

      out_image = lock.release();
      
      return yaRC_ok;
    }
    
    
    
    template <class pixel_t, int dim>
    yaRC writeRAW_helper(std::ofstream &f, const IImage*const& imin) {
    
      const Image<pixel_t, s_coordinate<dim> >* const pim = dynamic_cast<const Image<pixel_t, s_coordinate<dim> >*>(imin);
      if(pim == 0) {
        YAYI_DEBUG_MESSAGE("Error on the dynamic cast: image of type " + imin->Description());
        return yaRC_E_unknown;
      }
      
      offset size = total_number_of_points(pim->Size());
      
      f.write(reinterpret_cast<const char *>(&pim->pixel(0)), sizeof(pixel_t) * size);
    
      return f.fail() ? yaRC_E_file_io_error : yaRC_ok;
    }

    template <class pixel_t>
    yaRC writeRAW_helper_dim(std::ofstream &f, const IImage*const& imout) {
    
      int dim = get_last_dimension(imout->GetSize());

      switch(dim) {
        case 2:
          return writeRAW_helper<pixel_t, 2>(f, imout);
        case 3:
          return writeRAW_helper<pixel_t, 3>(f, imout);
        case 4:
          return writeRAW_helper<pixel_t, 4>(f, imout);
          
        default:
          return yaRC_E_not_implemented;
      }
    }
        
    yaRC writeRAW(const string_type &filename, const IImage*const &imin)
    {
      std::ofstream f(filename.c_str(), std::ios::binary);
      if(!f.is_open())
      {
        YAYI_DEBUG_MESSAGE("Unable to open file " + filename);
        return yaRC_E_file_io_error;
      }


      switch(imin->DynamicType().c_type) {
      case type::c_scalar:
      {
        switch(imin->DynamicType().s_type) {
        case type::s_ui8:  return writeRAW_helper_dim<yaUINT8> (f, imin); 
        case type::s_ui16: return writeRAW_helper_dim<yaUINT16>(f, imin); 
        case type::s_ui32: return writeRAW_helper_dim<yaUINT32>(f, imin); 
        case type::s_ui64: return writeRAW_helper_dim<yaUINT64>(f, imin); 
          
        case type::s_i8:   return writeRAW_helper_dim<yaINT8> (f, imin); 
        case type::s_i16:  return writeRAW_helper_dim<yaINT16>(f, imin); 
        case type::s_i32:  return writeRAW_helper_dim<yaINT32>(f, imin); 
        case type::s_i64:  return writeRAW_helper_dim<yaINT64>(f, imin); 
        
        case type::s_float:   return writeRAW_helper_dim<yaF_simple>(f, imin); break;
        case type::s_double:  return writeRAW_helper_dim<yaF_double>(f, imin); break;
        default:
          return yaRC_E_not_implemented;
        }
        
      }
      
      default:
        //delete temp;
        DEBUG_ASSERT(false, "unsupported type");
        return yaRC_E_not_implemented;
      }


      return yaRC_ok;
    }




  }
}

