/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <iostream>
#include <Yayi/core/yayiCommon/common_errors.hpp>
#include <Yayi/core/yayiCommon/include/common_types_T.hpp>

#ifndef NDEBUG
  #if defined(__APPLE__) || defined(__unix__)
  // demangle GCC
    #include <cxxabi.h>
  #endif
#endif

namespace yayi
{




	namespace errors
	{

		static std::ostream* yayi_error_stream_current = &std::cout;

		std::ostream& yayi_error_stream()
		{
			return *yayi_error_stream_current;
		}
    
    #ifndef NDEBUG
    
    #if defined(__APPLE__) || defined(__unix__)
    string_type demangle(const char* name)
    {
      // need to demangle C++ symbols
      std::size_t len; 
      int         stat;
      char* realname = __cxxabiv1::__cxa_demangle(name,NULL,&len,&stat);
      
      if (realname != NULL)
      {
        std::string out(realname);
        std::free(realname);
        return out;
      }
      return name;
    }
    
    #elif defined(_WIN32) && defined(_MSC_VER)

    // on visual
    //extern "C" char * _unDName(char * outputString, const char * name, int maxStringLength, void * (* pAlloc )(size_t), void (* pFree )(void *), unsigned short disableFlags);
    
    string_type demangle(const char* name) 
    {
      return name;
#if 0
      char * const pTmpUndName = _unDName(0, name, 0, malloc, free, 0); // last '0' for complete information
      if (pTmpUndName) 
      {
        std::string out(pTmpUndName);
        free(pTmpUndName);
        return out;
      }
      return name;
#endif
    }
    #endif
    
    #else
    string_type demangle(const char* name)
    {
      return name;
    }
    
    #endif
		


	}
}


