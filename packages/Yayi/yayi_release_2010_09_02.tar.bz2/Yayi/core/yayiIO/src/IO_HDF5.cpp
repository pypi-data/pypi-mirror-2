/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifdef YAYI_IO_HDF5_ENABLED__

#include "yayi_IO.hpp"
#include <Yayi/core/yayiImageCore/include/yayiImageCore_Impl.hpp>

#include "hdf5.h"
#include "hdf5_hl.h"

/*!@file
 * This file constains a wrapper to the HDF5 API\
 * @author Raffi Enficiaud
 */

namespace yayi {
  namespace IO {

    hid_t from_yayi_scalar_type_to_HDF5_type(const type& c)
    {
      switch(c.s_type)
      {
      case type::s_ui8:     return H5T_NATIVE_UCHAR;
      case type::s_i8:      return H5T_NATIVE_SCHAR;
      case type::s_ui16:    return H5T_NATIVE_USHORT;
      case type::s_i16:     return H5T_NATIVE_SHORT;
      case type::s_ui32:    return H5T_NATIVE_ULONG;
      case type::s_float:   return H5T_NATIVE_FLOAT;
      case type::s_double:  return H5T_NATIVE_DOUBLE;

      case type::s_i64:
      case type::s_ui64:
      case type::s_bool:
      default:
        break;
      }
      
      return -1;
    }
    
    yayi::type::scalar_type from_HDF5_scalar_type_to_yayi_scalar_type(const hid_t &t)
    {
      if(H5Tequal(t, H5T_NATIVE_UCHAR) > 0)  return type::s_ui8;
      if(H5Tequal(t, H5T_NATIVE_SCHAR) > 0)  return type::s_i8;
      if(H5Tequal(t, H5T_NATIVE_USHORT)> 0)  return type::s_ui16;
      if(H5Tequal(t, H5T_NATIVE_SHORT) > 0)  return type::s_i16;
      if(H5Tequal(t, H5T_NATIVE_ULONG) > 0)  return type::s_ui32;
      if(H5Tequal(t, H5T_NATIVE_FLOAT) > 0)  return type::s_float;
      if(H5Tequal(t, H5T_NATIVE_DOUBLE)> 0)  return type::s_double;
      
      #ifndef NDEBUG
      char debug_i[255];
      size_t len = 255;
      H5LTdtype_to_text(t, debug_i, H5LT_DDL, &len);
      DEBUG_INFO("None of the predefined data types does correspond to the provided one : " << debug_i);
      #endif
      return type::s_undefined;
    }
    
    
    hid_t from_yayi_compound_type_to_HDF5_type(const type& c)
    {
      hid_t scalar = from_yayi_scalar_type_to_HDF5_type(c);
      if(scalar == -1)
        return -1;
      
      herr_t status = H5Tset_order(scalar, H5T_ORDER_LE); // do something with this order
      if(status < 0)
      {
        H5Tclose(scalar); 
        return -1;
      }
        
      
      switch(c.c_type)
      {
        case type::c_scalar:
          return scalar;
        case type::c_3:
        {
          static const hsize_t adims[] = {1,1,1};  
          return H5Tarray_create(scalar, 3, adims);
        }
        case type::c_4:
        {
          static const hsize_t adims[] = {1,1,1,1};  
          return H5Tarray_create(scalar, 4, adims);
        }
        case type::c_complex:
        {
          static const hsize_t adims[] = {1,1};
          //hid_t complex_id = H5Tcreate (H5T_COMPOUND, sizeof tmp);
          //H5Tinsert (complex_id, "real", HOFFSET(tmp,re), H5T_NATIVE_DOUBLE);
          //H5Tinsert (complex_id, "imaginary", HOFFSET(tmp,im), H5T_NATIVE_DOUBLE);
          return H5Tarray_create(scalar, 2, adims);
        }

        default:
          break;
      }
      return -1;
    }
    
    yayi::type from_HDF5_type_to_yayi_compound_type(const hid_t &t)
    {
      hid_t order = H5Tget_order(t);
      if (order != H5T_ORDER_LE)
      {
        errors::yayi_error_stream() << YAYI_DEBUG_MESSAGE("Order different from little endian: unsupported") << std::endl;
        return type_undefined;
      }

      
      yayi::type::scalar_type s = from_HDF5_scalar_type_to_yayi_scalar_type(t);//scalar_hid);
      if(s == type::s_undefined)
      {
        DEBUG_INFO("Type returned by from_HDF5_scalar_type_to_yayi_scalar_type is undefined");
        return type_undefined;
      }
      
      hid_t scalar_hid = H5Tget_class(t);
      if (scalar_hid == H5T_INTEGER || scalar_hid == H5T_FLOAT)
      {
        //std::cout << "Data set SCALAR type" << std::endl;
        return type(type::c_scalar, s);
      }
        
        
      // dimensions
      int dims_data = H5Tget_array_ndims(t);
      if(dims_data < 1 || dims_data > 4)
        return type_undefined;
      
      // taille
      hsize_t *ss = new hsize_t[dims_data];
      if(H5Tget_array_dims(t, ss) < 0)
      {
        DEBUG_INFO("An error occured in H5Tget_array_dims");
        delete [] ss;
        return type_undefined;
      }
      
      for(int i = 0; i < dims_data; i++)
      {
        if(ss[i] != 1)
        {
          DEBUG_INFO("The dimension " << i << " has not a size of 1");
          delete [] ss;
          return type_undefined;         
        }
      }
      delete [] ss;
      
      if(dims_data == 1)
        return type(type::c_scalar, s);
      else if(dims_data == 2)
        return type(type::c_complex, s);
      else if(dims_data == 3)
        return type(type::c_3, s);
      else if(dims_data == 4)
        return type(type::c_4, s);
      return type_undefined;
    }
    
    hsize_t * from_coordinate_to_HDF5_dimension(const IImage::coordinate_type& s)
    {
      hsize_t* arr = new hsize_t[s.dimension()];
      for(unsigned int i = 0; i < s.dimension(); i++)
        arr[i] = s[s.dimension() - i - 1];
      return arr;
    }

    IImage::coordinate_type from_HDF5_dimension_to_coordinate(hid_t data_space_id)
    {
      int rank = H5Sget_simple_extent_ndims(data_space_id);
      hsize_t * ss = new hsize_t[rank];
      hsize_t * mss = new hsize_t[rank];
      if(H5Sget_simple_extent_dims(data_space_id, ss, mss) < 0)
      {
        delete [] ss; delete [] mss;
        return IImage::coordinate_type();
      }
      
      IImage::coordinate_type ret;
      ret.set_dimension(rank);
      for(int i = 0; i < rank; i++)
        ret[i] = ss[rank - i - 1];
      delete [] ss; delete [] mss;
      return ret;
    }
    
    
    template <class image_t>
    yaRC hdf5_write_helper(const IImage* const& im_interface, hid_t& data_id, hid_t& data_type) {
      const image_t* im = dynamic_cast<const image_t*>(im_interface);
      if(im == 0)
        return yaRC_E_bad_parameters;
      herr_t status = H5Dwrite(data_id, data_type, H5S_ALL, H5S_ALL, H5P_DEFAULT, reinterpret_cast<const void*>(&im->pixel(0)));
      return status < 0 ? yaRC_E_file_io_error : yaRC_ok;
    }
    

    
    #if 0
    template <class image_t, int current_dim>
    struct hdf5_table_pointer
    {
    
      // boost::multi_array<typename image_t::pixel_type*, image_t::coordinate_type::static_dimensions> &table
    
      template <class arr_t>
      yaRC operator()(
        image_t& im, 
        arr_t &table,
        typename image_t::coordinate_type const& s = typename image_t::coordinate_type(0) )
      {
        hdf5_table_pointer<image_t, current_dim-1> op_bis;
        for(int i = 0; i < im.Size()[current_dim]; i ++)
        {
          typename image_t::coordinate_type ss(s);
          ss[current_dim] = i;
          op_bis(im, ss, table);
        }
        
        return yaRC_ok;
      }
   
    };

    template <class image_t>
    struct hdf5_table_pointer<image_t, 1>
    {
    
      yaRC operator()(image_t& im, typename image_t::coordinate_type const& s, void** table)
      {
        const int current_dim = 1;
        
        for(int i = 0; i < im.Size()[current_dim]; i ++)
        {
          typename image_t::coordinate_type ss(s);
          ss[current_dim] = i;
          reinterpret_cast<void **>(*table)[i] = &im.pixel(ss);
        }
        
        return yaRC_ok;
      }

      yaRC del(image_t& im, typename image_t::coordinate_type const& s, void** table)
      {
        delete [] *table;
        return yaRC_ok;
      }

    };
    
    #endif
    
    template <class image_t>
    yaRC hdf5_read_helper(IImage*& im_interface, hid_t& data_id, hid_t& data_type, hid_t& filespace_id) {
    
      assert(im_interface);
      image_t* im = dynamic_cast<image_t*>(im_interface);
      if(im == 0)
      {
        DEBUG_INFO("An error occured during the dynamic cast of the image " << im_interface->Description());
        return yaRC_E_bad_parameters;
      }
      
      hsize_t *s = from_coordinate_to_HDF5_dimension(im->Size());//{total_number_of_points(im->Size())};
      hid_t mem_data_space = H5Screate_simple(im->GetDimension(), s, 0);
      
      herr_t status = H5Dread(data_id, data_type, mem_data_space, filespace_id, H5P_DEFAULT, reinterpret_cast<void*>(&im->pixel(0)));
      #ifndef NDEBUG
      if(status < 0)
      {
        DEBUG_INFO("status error for H5Dread : " << status);
        char debug_i[255];
        size_t len = 255;
        H5LTdtype_to_text(data_type, debug_i, H5LT_DDL, &len);
        
      }
      #endif
      H5Sclose(mem_data_space);
      delete [] s;
      return status < 0 ? yaRC_E_file_io_error : yaRC_ok;
    }  
    

    yaRC writeHDF5(const std::string &filename, const IImage* const& im, const std::string &image_name /* = image_yayi */) 
    {
      
      if(im == 0)
        return yaRC_E_null_pointer;

      hid_t data_type_id = from_yayi_compound_type_to_HDF5_type(im->DynamicType());
      if(data_type_id == -1)
      {
        DEBUG_INFO("An error occured while creating the datatype id");
        return yaRC_E_unknown;
      }
      
      // create a new HDF5 file using default properties
      hid_t file_id = H5Fcreate( filename.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT );
      if(file_id < 0)
      {
        DEBUG_INFO("Unable to create the file: error " << (int)file_id);
        return yaRC_E_file_io_error;
      }

      // create an array of the appropriate coordinates
      hsize_t *dims = from_coordinate_to_HDF5_dimension(im->GetSize());
      hid_t data_space_id = H5Screate_simple(im->GetSize().dimension(), dims, NULL);
      delete [] dims;
      if(data_space_id < 0)
      {
        DEBUG_INFO("Unable to create the dataspace: error " << (int)data_space_id);
        H5Sclose(data_type_id);
        H5Sclose(file_id);
        return yaRC_E_file_io_error;
      }
      
           
      hid_t dataset_id = H5Dcreate(file_id, image_name.c_str(), data_type_id, data_space_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT); 
      if(dataset_id < 0)
      {
        DEBUG_INFO("Unable to create the dataset: error " << (int)dataset_id);
        H5Sclose(data_type_id);
        H5Sclose(data_space_id);
        H5Sclose(file_id);
        return yaRC_E_file_io_error;
      }

      yaRC res = yaRC_ok;
      
      switch(im->DynamicType().c_type)
      {
      case type::c_scalar:
        switch(im->DynamicType().s_type)
        {
        case type::s_ui8:
          res = hdf5_write_helper< Image<yaUINT8> >(im, data_space_id, data_type_id);
          break;
        
        default:
          DEBUG_INFO("Unsupported scalar type: " << im->DynamicType());
          break;
        }
        

      default:
        DEBUG_INFO("Unsupported compound type: " << im->DynamicType());
        break;
      }


      
      H5Tclose(data_type_id); 
      H5Dclose(dataset_id); 
      H5Sclose(data_space_id);
      H5Sclose(file_id);


      return res;
    }


    yaRC readHDF5(const std::string &filename, IImage*& im, const std::string &image_name /* = image_yayi */) 
    {
       if(im != 0)
        return yaRC_E_null_pointer;

      hid_t file_id = H5Fopen(filename.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
      if(file_id < 0)
      {
        DEBUG_INFO("Unable to open the file: error " << (int)file_id);
        return yaRC_E_file_io_error;
      }

      hid_t dataset_id = H5Dopen(file_id, image_name.c_str(), H5P_DEFAULT);
      if(dataset_id < 0)
      {
        DEBUG_INFO("Unable to open the dataset within the file: error " << (int)dataset_id << " / dataset name: " << image_name);
        return yaRC_E_file_io_error;
      }



      // datatype identifier 
      hid_t data_type_id = H5Dget_type(dataset_id); 

      #ifndef NDEBUG
      {
        char debug_i[255];
        size_t len = 255;
        H5LTdtype_to_text(data_type_id, debug_i, H5LT_DDL, &len);
        DEBUG_INFO("dataset type : " << debug_i);
      }
      #endif  
      
      // mapping to yayi type
      yayi::type t = from_HDF5_type_to_yayi_compound_type(data_type_id);
      if(t == yayi::type_undefined)
      {
        DEBUG_INFO("An error occured while getting the type of the stored array");
        H5Tclose(data_type_id); 
        H5Dclose(dataset_id);
        H5Fclose(file_id);
        return yaRC_E_unknown;
      }
      
      // dataspace identifier
      hid_t data_space_id = H5Dget_space(dataset_id);

      // dimensions of the array
      int dim = H5Sget_simple_extent_ndims(data_space_id);
      if(dim < 0)
      {
        DEBUG_INFO("An error occured while getting the dimension of the dataspace");
        H5Sclose(data_space_id);
        H5Tclose(data_type_id); 
        H5Dclose(dataset_id);
        H5Fclose(file_id);
        return yaRC_E_unknown;       
      }
      
      im = IImage::Create(t, dim);
      if(im == 0)
      {
        DEBUG_INFO("An error occured during the creation of the image");
        H5Sclose(data_space_id);
        H5Tclose(data_type_id); 
        H5Dclose(dataset_id);
        H5Fclose(file_id);
        return yaRC_E_unknown;
      }
      
      IImage::coordinate_type size = from_HDF5_dimension_to_coordinate(data_space_id);
      
      yaRC res = im->SetSize(size);
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured while setting the size of the image: size: " << size << " error: " << res);
        H5Sclose(data_space_id);
        H5Tclose(data_type_id); 
        H5Dclose(dataset_id);
        H5Fclose(file_id);
        return yaRC_E_unknown;       
      }
      
      res = im->AllocateImage();
      if(res != yaRC_ok)
      {
        DEBUG_INFO("An error occured while allocating the image: error: " << res);
        H5Sclose(data_space_id);
        H5Tclose(data_type_id); 
        H5Dclose(dataset_id);
        H5Fclose(file_id);
        return yaRC_E_unknown;       
      }     

      
      switch(t.c_type)
      {
      case type::c_scalar:
        switch(t.s_type)
        {
        case type::s_ui8:
          res = hdf5_read_helper< Image<yaUINT8, s_coordinate<3> > >(im, dataset_id, data_type_id, data_space_id);
          break;
        
        case type::s_float:
          res = hdf5_read_helper< Image<yaF_simple, s_coordinate<3> > >(im, dataset_id, data_type_id, data_space_id);
          break;            

        case type::s_double:
          res = hdf5_read_helper< Image<yaF_double, s_coordinate<3> > >(im, dataset_id, data_type_id, data_space_id);
          break;                  
            
        default:
          DEBUG_INFO("Unsupported scalar type: " << t);
          res = yaRC_E_not_implemented;
          break;
        }
        break;
        

      default:
        DEBUG_INFO("Unsupported compound type: " << t);
        res = yaRC_E_not_implemented;
        break;
      }

      H5Sclose(data_space_id);
      H5Tclose(data_type_id); 
      H5Dclose(dataset_id);
      H5Fclose(file_id);
      
      if(res != yaRC_ok) {
        delete im;
        im = 0;
      }
      
      return res;
      

    }
}} // namespace 

#endif
