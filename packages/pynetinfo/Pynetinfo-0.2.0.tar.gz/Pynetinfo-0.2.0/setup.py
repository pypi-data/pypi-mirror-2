#    Pynetinfo - A python module for controlling linux network interfaces
#    Copyright (C) 2010  Sassan Panahinejad (sassan@sassan.me.uk) 
#    www.sassan.me.uk
#    pypi.python.org/pypi/pynetinfo/

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from distutils.core import setup, Extension

module1 = Extension('netinfo',
                    sources = ['netinfo.c', 'iface.c', 'route.c'])

setup (name = 'Pynetinfo',
       version = '0.2.0',
       description = 'python network information',
       ext_modules = [module1])
