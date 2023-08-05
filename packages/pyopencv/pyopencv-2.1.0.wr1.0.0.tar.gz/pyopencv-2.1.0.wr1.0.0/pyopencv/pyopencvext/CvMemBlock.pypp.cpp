// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "boost/python/object.hpp"
#include "CvMemBlock.pypp.hpp"

namespace bp = boost::python;

static ::CvMemBlock * get_prev( ::CvMemBlock const & inst ) { return inst.prev; }

static ::CvMemBlock * get_next( ::CvMemBlock const & inst ) { return inst.next; }

void register_CvMemBlock_class(){

    bp::class_< CvMemBlock >( "CvMemBlock" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvMemBlock >() )    
        .add_property( "prev", bp::make_function(&::get_prev, bp::return_internal_reference<>()) )    
        .add_property( "next", bp::make_function(&::get_next, bp::return_internal_reference<>()) );

}
