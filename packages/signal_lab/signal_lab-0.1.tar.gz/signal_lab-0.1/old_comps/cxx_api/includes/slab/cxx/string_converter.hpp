/*
  Copyright (C) 2008 Gilles Hennenfent and Sean Ross-Ross

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#ifndef _SLAB_STRING_CONVERTER_HPP
#define _SLAB_STRING_CONVERTER_HPP

#include <string>
#include <sstream>

namespace signal_lab
{

	using namespace std;

	template <class T>
	class StringConvert
	{
	public:
		static bool from_string(T& t, const std::string& s )
		{
		  std::istringstream iss(s);
		  return !(iss >> t).fail();
		}

		static string to_string( T& t )	{
		  ostringstream oss;
		  oss << t;
		  return oss.str( );
		}

	};

}

#endif //_SLAB_STRING_CONVERTER_HPP
