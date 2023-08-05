// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "CvRect.pypp.hpp"

namespace bp = boost::python;

void register_CvRect_class(){

    bp::class_< CvRect >( "CvRect" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvRect >() )    
        .def_readwrite( "height", &CvRect::height )    
        .def_readwrite( "width", &CvRect::width )    
        .def_readwrite( "x", &CvRect::x )    
        .def_readwrite( "y", &CvRect::y );

}
