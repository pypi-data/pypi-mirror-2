/*
  Copyright (C) 2008 The University of British Columbia

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

/*!
\mainpage
\section whatis Introduction

SLab provides the signal processing community with a
reproducible research framework for computational
experiments.

It can help you in three ways:

\arg SLab core: write your own command line program,
\arg SLab contrib: use the contributions of other
users to process your data,
\arg SLab repro: organize and document your research
so that other users can learn and use it.

\section features Features

Here is a list of some of SLab's most interesting features:
\arg distributed file format to handle HUGE data (e.g., seismic data),
\arg portable to any platform with a C++ compiler and Python,
\arg extensive documentation (HTML, PDF, and man pages)
from documented source files using Doxygen
(http://www.stack.nl/~dimitri/doxygen),
\arg C++ and Python (soon) interfaces,
\arg free software, released under the GNU General Public
License (GPL, see SLab license).

\section doc Documentation

HTML, PDF, and man pages

\section download Downloading
\subsection tarball Tarball

You can download at http://www.xxx.yyy/SLab.tar.gz the
current snapshot of SLab source code. Unpack the
archive as follows

@code
tar -xvzf something.tar.gz dir_you_want
@endcode

\subsection svn Subversion

You can also download the development version of SLab using a
Subversion (http://subversion.tigris.org) client. Proceed as
follows

@code
svn co https://www.xxx.yyy/slab/trunk dir_you_want
@endcode

If you encounter any problem, refer to the \ref faq "Troubleshooting page".

\section ack Acknowledgments

\section links Related links

\arg Madagascar (http://rsf.sourceforge.net)

\section feedback Feedback

If you have comments, questions, or suggestions regarding SLab,
don't hesitate to email us at xxx@xxx.xxx.

\authors Gilles Hennenfent, Ph.D.
\authors Sean Ross-Ross
 */


/*!
 * \page referenceguide Reference Guide
 *
 * \arg \ref  components "SLAB components reference"
 * this contains API reference for all SLAB components.
 * what is a SLAB component?
 *
 * \arg \ref  SLABmains "SLAB Main Programs Reference"
 * paruse through the main programs
 *
 * \arg \ref compiletools "Compile Time Tools"
 * SCons tool objects to ease compilation

 * \arg \ref reprotool
 * Scons Tools for generating reproducible research
 *
 * \arg \ref sconsbuilders
 * SLAB SCons builders
 *
 */

/*!
 * \page elem Element Wise Operations
 * This page contains SLAB main programs that perform element-wise operations on slab/RSF files
 */

/*!
 * \page SLABmains SLAB Main Programs
 * This page contains a list of main programs
 * \see \ref elem for programs that do element wise operations on data
 * \see \ref usermains for programs sorted by user
 *
 * \section mainprogssec Main Programs
 */

/*!
 * \page sconsbuilders SConstruct Compile-Time Builders
 * This page contains a list of SCons Builders that are added to RSF with various SCons Tools for
 * the creation of slab programs
 */

/*!
 * \page sconstools SConstruct Tools
 * This page contains a list of SConstruct tools
 * added by the SLAB project.
 */

/*!
 * \page sbldrs SCons Builders
 * This page contains a list of SConstruct Builders that are used for reproducability
 * added by the SLAB project.
 */

/*!
 * \page compiletools Compile Time Tools
 * This page contains tools to help compile signal process
 */

/*!
 * \page reprotool Reproducible Research Tools
 * This page contains tools to help with reproducible research
 */

/*!
 * \page components SLAB components
 * These components are built up from nothing
 */

/*!
 \page sbooks Signal Processing Laboratory 'Books'
 Books is a collection of use cases for main programs in SLAB

 */
