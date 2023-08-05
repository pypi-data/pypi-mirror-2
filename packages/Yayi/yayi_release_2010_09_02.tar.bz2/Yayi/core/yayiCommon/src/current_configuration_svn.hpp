/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_CURRENT_CONFIGURATION_SVN_HPP__
#define YAYI_CURRENT_CONFIGURATION_SVN_HPP__


/*!@file 
 * Template used with the SVN (TortoiseSVN) version retrieval facility
 * @author Raffi Enficiaud
 */

namespace yayi
{
  const char *svn_revision_version  = "$WCREV$";
  const char *svn_revision_date     = "$WCDATE$";
}


#endif